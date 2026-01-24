import os
import sys
import subprocess
import argparse
import tempfile
import time
import re
import zipfile
import shutil
import io
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Global tqdm and rich handle for safe access
try:
    from tqdm import tqdm
except ImportError:
    tqdm = None

try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
    from rich.panel import Panel
    from rich.live import Live
    from rich.table import Table
    console = Console()
except ImportError:
    console = None
    Progress = None

# ==========================================
# AUTO-DEPENDENCY INSTALLER
# ==========================================
def install_dependencies():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    req_path = os.path.abspath(os.path.join(script_dir, "..", "requirements.txt"))
    
    print(f"[System] Missing dependencies detected. Installing from {req_path}...")
    
    if not os.path.exists(req_path):
        print(f"[Error] requirements.txt not found at {req_path}")
        sys.exit(1)
        
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
        print("[System] Dependencies installed. Restarting script...")
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to install dependencies: {e}")
        sys.exit(1)

try:
    import requests
    from bs4 import BeautifulSoup
    import html2text
    import docx
    import pypdf
    # OCR and Image support
    from rapidocr_onnxruntime import RapidOCR
    import cv2 
    from PIL import Image
    # COM for .doc
    import win32com.client
    import pythoncom
except ImportError:
    install_dependencies()

# Re-import after ensure
import requests
from bs4 import BeautifulSoup
import html2text
import docx
import pypdf
from rapidocr_onnxruntime import RapidOCR
# win32com might fail on non-windows, handle gracefully later

# ==========================================
# CONFIGURATION
# ==========================================
class Config:
    MAX_CHARS_DEFAULT = 50000
    TRUNCATION_MSG = "\n\n[SYSTEM: CONTENT TRUNCATED DUE TO LENGTH LIMIT]"
    
    @staticmethod
    def get_script_dir():
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def get_config_dir():
        path = os.path.join(Config.get_script_dir(), "..", "config")
        os.makedirs(path, exist_ok=True)
        return path

    @staticmethod
    def get_browser_config_path():
        return os.path.join(Config.get_config_dir(), "browser_path.txt")
    
    @staticmethod
    def get_output_path():
        return os.path.join(Config.get_config_dir(), "raw_content.txt")

    @staticmethod
    def get_browser_path():
        config_file = Config.get_browser_config_path()
        default_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        ]
        
        def read_path():
            if not os.path.exists(config_file): return None
            with open(config_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"): return line
            return None

        current = read_path()
        if current: return current

        detected = next((p for p in default_paths if os.path.exists(p)), default_paths[0])
        
        # Write default
        content = f"""# Browser Configuration
# Please paste your browser executable path below:
{detected}
"""
        try:
            with open(config_file, "w", encoding="utf-8") as f: f.write(content)
        except: pass
        
        return detected

# ==========================================
# LOGGING
# ==========================================
def log(msg, style="blue"):
    if console:
        console.print(f"[bold {style}][Ingester][/bold {style}] {msg}")
    else:
        print(f"[Ingester] {msg}")

def log_success(msg):
    log(msg, "green")

def log_error(msg):
    log(msg, "red")

def log_warning(msg):
    log(msg, "yellow")

# ==========================================
# BROWSER DRIVER
# ==========================================
class BrowserDriver:
    @staticmethod
    def lazy_import_drission():
        try:
            from DrissionPage import ChromiumPage, ChromiumOptions
            return ChromiumPage, ChromiumOptions
        except ImportError:
            return None, None

    @staticmethod
    def fetch_html(url):
        log(f"Switching to DrissionPage for: {url}")
        ChromiumPage, ChromiumOptions = BrowserDriver.lazy_import_drission()
        if not ChromiumPage:
            return None, "[SYSTEM: DrissionPage not installed]"

        page = None
        try:
            co = ChromiumOptions()
            path = Config.get_browser_path()
            if path and os.path.exists(path):
                co.set_browser_path(path)
            
            # [LCS-FIX] 2026-01-23: Disable headless to bypass 403/404 on Zhihu/Cloudflare
            co.headless(False) 
            co.set_argument('--no-sandbox')
            co.set_argument('--disable-gpu')
            co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            page = ChromiumPage(co)
            page.get(url)
            time.sleep(3)
            
            # [LCS-FIX] 2026-01-25: Multi-scroll to trigger CSDN/Zhihu lazy loading
            for i in range(3):
                log(f"Scrolling ({i+1}/3)...")
                page.scroll.to_bottom()
                time.sleep(2)
            
            # [LCS-FIX] Handling Zhihu/Generic Login Popups
            try:
                # Zhihu specific close button class
                close_btn = page.ele('.Modal-closeButton', timeout=2)
                if close_btn:
                    log("Detected Zhihu Login Popup. Smashing it.")
                    close_btn.click()
                    time.sleep(1)
            except Exception:
                pass
                
            return page.html, None
        except Exception as e:
            if page: 
                try: page.quit()
                except: pass
            return None, str(e)

# ==========================================
# CONTENT PARSER
# ==========================================
class ContentParser:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.ocr_engine = None
        self.drission_lock = threading.Lock()

    def get_ocr_engine(self):
        if not self.ocr_engine:
            try:
                self.ocr_engine = RapidOCR()
            except Exception as e:
                log(f"Failed to initialize RapidOCR: {e}")
        return self.ocr_engine

    def perform_ocr(self, img_path):
        engine = self.get_ocr_engine()
        if not engine: return "[OCR Failed: Engine not available]"
        
        try:
            result, _ = engine(img_path)
            if result:
                text = "\n".join([line[1] for line in result])
                return text
            return "[OCR: No text found]"
        except Exception as e:
            return f"[OCR Error: {e}]"

    def clean_html(self, html, base_url=""):
        # Fix encoding if needed (UTF-8)
        if isinstance(html, bytes):
            html = html.decode('utf-8', errors='replace')
        else:
            # Check for mojibake (UTF-8 bytes misread as Latin-1)
            try:
                # If it's already a string, check if it contains characters that look like misread UTF-8
                # Common pattern: multiple high-byte characters in a row
                if any(ord(c) > 127 for c in html):
                    # Attempt to re-encode to bytes then decode properly
                    test_html = html.encode('latin-1').decode('utf-8')
                    # If it decoded without error and changed the string, use it
                    if test_html != html:
                        html = test_html
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass

        if not html2text:
            log("html2text not installed. Falling back to simple text extraction.")
            soup = BeautifulSoup(html, 'html.parser')
            for s in soup(["script", "style", "nav", "footer", "iframe"]): s.decompose()
            return soup.get_text(separator='\n', strip=True)

        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0 # No wrapping
        h.protect_links = True
        h.base_url = base_url
        return h.handle(html)

    def extract_metadata(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "Untitled"
        # Try to find author (Generic)
        author = "Unknown"
        meta_author = soup.find("meta", attrs={"name": "author"})
        if meta_author: author = meta_author.get("content")
        return f"Title: {title}\nAuthor: {author}\nDate: {time.strftime('%Y-%m-%d')}\n"

    def process_url(self, url):
        log(f"Fetching: {url}")
        html = ""
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=15)
            if resp.status_code in [403, 429, 503]:
                log(f"Requests {resp.status_code}. Invoking DrissionPage.")
                with self.drission_lock:
                    html, err = BrowserDriver.fetch_html(url)
                if not html: return f"Error: {err}"
            else:
                resp.raise_for_status()
                html = resp.text
        except Exception as e:
            log(f"Requests failed: {e}. Invoking DrissionPage.")
            with self.drission_lock:
                html, err = BrowserDriver.fetch_html(url)
            if not html: return f"Error: {err}"

        meta = self.extract_metadata(html)
        markdown = self.clean_html(html, base_url=url)
        
        return f"{meta}\n=== CONTENT ===\n{markdown}"

    def extract_images_from_docx(self, file_path):
        """Extracts images from docx and performs OCR (Concurrent)"""
        log("Extracting images from DOCX for OCR...")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # Find image files
                    image_files = [f for f in zip_ref.namelist() if f.startswith('word/media/') and f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
                    image_files.sort() # Keep order
                    
                    if not image_files:
                        log("No images found in DOCX.")
                        return ""

                    log(f"Found {len(image_files)} images. Processing concurrently...")
                    
                    results_map = {}
                    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                        future_to_img = {}
                        for i, img_file in enumerate(image_files):
                            # Extract
                            zip_ref.extract(img_file, temp_dir)
                            full_path = os.path.join(temp_dir, img_file)
                            future_to_img[executor.submit(self.perform_ocr, full_path)] = (i, img_file)
                        
                        for future in as_completed(future_to_img):
                            idx, img_name = future_to_img[future]
                            try:
                                text = future.result()
                                if text and not text.startswith("[OCR"):
                                    results_map[idx] = f"\n[IMAGE {idx+1} CONTENT (OCR)]:\n{text}\n"
                                else:
                                    results_map[idx] = f"\n[IMAGE {idx+1}]: {text}\n"
                            except Exception as e:
                                results_map[idx] = f"\n[IMAGE {idx+1}]: OCR Error: {e}\n"
                            
            except zipfile.BadZipFile:
                log("Failed to unzip DOCX. Is it valid?")
                return "\n[ERROR: Failed to extract images from DOCX]"
                
        # Combine in order
        ocr_results = [results_map[i] for i in range(len(image_files))]
        return "\n=== DETECTED IMAGE TEXT ===\n" + "\n".join(ocr_results) if ocr_results else ""

    def _extract_docx_content(self, file_path):
        # Text extraction
        doc = docx.Document(file_path)
        text_content = '\n'.join([para.text for para in doc.paragraphs])
        
        # Image OCR extraction
        image_content = self.extract_images_from_docx(file_path)
        
        return text_content + "\n" + image_content

    def _process_pdf_page(self, page_idx, page):
        """Processes a single PDF page: text + images (OCR)"""
        content = ""
        # Text
        page_text = page.extract_text()
        if page_text:
            content += f"\n=== PAGE {page_idx+1} TEXT ===\n{page_text}\n"
        
        # Images
        try:
            images = page.images
            if images:
                for j, image in enumerate(images):
                    ext = os.path.splitext(image.name)[1] or ".png"
                    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_img:
                        tmp_img.write(image.data)
                        tmp_img_path = tmp_img.name
                    
                    ocr_text = self.perform_ocr(tmp_img_path)
                    if ocr_text and not ocr_text.startswith("[OCR") and not ocr_text.startswith("[OCR: No text"):
                        content += f"\n[PAGE {page_idx+1} IMAGE {j+1} CONTENT (OCR)]:\n{ocr_text}\n"
                    
                    try: os.remove(tmp_img_path)
                    except: pass
        except Exception as img_err:
            log(f"Error extracting images from page {page_idx+1}: {img_err}")
            
        return content

    def _extract_pdf_content(self, file_path):
        log(f"Extracting content from PDF: {file_path} (Concurrent)")
        try:
            reader = pypdf.PdfReader(file_path)
            num_pages = len(reader.pages)
            log(f"PDF has {num_pages} pages. Processing concurrently...")
            
            results_map = {}
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                future_to_page = {executor.submit(self._process_pdf_page, i, reader.pages[i]): i for i in range(num_pages)}
                
                for future in as_completed(future_to_page):
                    idx = future_to_page[future]
                    try:
                        results_map[idx] = future.result()
                    except Exception as e:
                        results_map[idx] = f"\n[ERROR processing PAGE {idx+1}: {e}]"
            
            # Combine in order
            full_content = "".join([results_map[i] for i in range(num_pages)])
            return full_content
                    
        except Exception as e:
            return f"\n[ERROR processing PDF: {e}]"

    def convert_doc_to_docx(self, doc_path):
        try:
            import win32com.client
            import pythoncom
        except ImportError:
            return None, "pywin32 not installed. Cannot process .doc files."

        word = None
        temp_docx = os.path.join(tempfile.gettempdir(), f"converted_{int(time.time())}.docx")
        try:
            # Initialize COM
            pythoncom.CoInitialize()
            try:
                word = win32com.client.Dispatch("Word.Application")
            except Exception:
                # Try dispatch ex if standard dispatch fails (sometimes helps)
                word = win32com.client.DispatchEx("Word.Application")
            
            if not word: return None, "Failed to initialize Word Application"

            word.Visible = False
            word.DisplayAlerts = 0
            
            doc = word.Documents.Open(os.path.abspath(doc_path))
            doc.SaveAs2(temp_docx, FileFormat=16) # 16 = wdFormatXMLDocument (docx)
            doc.Close()
            return temp_docx, None
        except Exception as e:
            return None, str(e)
        finally:
            if word:
                try: word.Quit()
                except: pass

    def process_file(self, file_path):
        log(f"Processing file: {file_path}")
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        ext = os.path.splitext(file_path)[1].lower()
        filename = os.path.basename(file_path)
        meta = f"Title: {filename}\nSource: Local File\nDate: {time.strftime('%Y-%m-%d')}\n"
        content = ""

        try:
            if ext == '.txt':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
            
            elif ext == '.docx':
                content = self._extract_docx_content(file_path)
            
            elif ext == '.doc':
                log("Detected .doc file. Attempting conversion to .docx...")
                temp_docx, err = self.convert_doc_to_docx(file_path)
                if temp_docx and os.path.exists(temp_docx):
                    content = self._extract_docx_content(temp_docx)
                    # Cleanup
                    try: os.remove(temp_docx)
                    except: pass
                else:
                    return f"{meta}\n=== ERROR ===\nFailed to convert .doc file: {err}\nPlease ensure Microsoft Word is installed or convert to .docx manually."

            elif ext == '.pdf':
                content = self._extract_pdf_content(file_path)
            
            elif ext in ['.jpg', '.jpeg', '.png', '.bmp']:
                # Direct image OCR
                content = self.perform_ocr(file_path)
            
            else:
                log(f"Unknown extension {ext}, trying as text...")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    return f"{meta}\n=== ERROR ===\nUnsupported file format: {ext}"

        except Exception as e:
            # import traceback
            # traceback.print_exc()
            return f"{meta}\n=== ERROR ===\nFailed to process file: {str(e)}"

        return f"{meta}\n=== CONTENT ===\n{content}"

# ==========================================
# MAIN
# ==========================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", help="One or more URLs or Local File Paths")
    args = parser.parse_args()
    
    cp = ContentParser()
    
    log(f"Starting ingestion for {len(args.inputs)} items...", style="cyan")
    
    results_map = {}
    max_workers = os.cpu_count() or 4
    
    if Progress:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=None, pulse_style="bright_blue"),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True
        ) as progress:
            main_task = progress.add_task("[cyan]Overall Progress", total=len(args.inputs))
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_input = {}
                for i, inp in enumerate(args.inputs):
                    if os.path.exists(inp) and os.path.isfile(inp):
                        future_to_input[executor.submit(cp.process_file, inp)] = i
                    else:
                        if not inp.startswith(('http://', 'https://')):
                            if not inp.startswith('http'):
                                inp = 'https://' + inp
                        future_to_input[executor.submit(cp.process_url, inp)] = i
                
                for future in as_completed(future_to_input):
                    idx = future_to_input[future]
                    try:
                        results_map[idx] = future.result()
                        log_success(f"Completed: {args.inputs[idx][:50]}...")
                    except Exception as e:
                        results_map[idx] = f"Error processing input {args.inputs[idx]}: {e}"
                        log_error(f"Failed: {args.inputs[idx][:50]}... Error: {e}")
                    progress.update(main_task, advance=1)
    else:
        # Fallback to tqdm or simple loop
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_input = {}
            for i, inp in enumerate(args.inputs):
                if os.path.exists(inp) and os.path.isfile(inp):
                    future_to_input[executor.submit(cp.process_file, inp)] = i
                else:
                    if not inp.startswith(('http://', 'https://')):
                        if not inp.startswith('http'):
                            inp = 'https://' + inp
                    future_to_input[executor.submit(cp.process_url, inp)] = i
            
            iterable = as_completed(future_to_input)
            if tqdm is not None:
                iterable = tqdm(iterable, total=len(args.inputs), desc="Ingesting Content")
                
            for future in iterable:
                idx = future_to_input[future]
                try:
                    results_map[idx] = future.result()
                except Exception as e:
                    results_map[idx] = f"Error processing input {args.inputs[idx]}: {e}"
    
    # Combine results
    final_output = ""
    for i in range(len(args.inputs)):
        source_url = args.inputs[i]
        content = results_map.get(i, "Error: Content missing")
        
        separator = f"\n\n" + "="*60 + "\n"
        separator += f"--- SOURCE {i+1}: {source_url} ---\n"
        separator += "="*60 + "\n\n"
        
        final_output += separator + content
    
    output_path = Config.get_output_path()
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_output)
        log_success(f"All content saved to: {output_path}")
        
        if console:
            console.print(Panel(f"[bold green]Ingestion Complete![/bold green]\nProcessed [cyan]{len(args.inputs)}[/cyan] sources.", title="Success", expand=False))
            
    except Exception as e:
        log_error(f"Failed to save output: {e}")

if __name__ == "__main__":
    main()

import os
import sys
import subprocess
import argparse
import tempfile
import time
import re

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
except ImportError:
    install_dependencies()

# Re-import after ensure
import requests
from bs4 import BeautifulSoup
import html2text

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
def log(msg):
    print(f"[Ingester] {msg}")

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
            
            co.headless(True)
            co.set_argument('--no-sandbox')
            co.set_argument('--disable-gpu')
            co.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
            
            page = ChromiumPage(co)
            page.get(url)
            time.sleep(2)
            
            # Anti-bot check
            title = page.title.lower() if page.title else ""
            if any(x in title for x in ["just a moment", "access denied", "attention required"]):
                log("Challenge detected, waiting...")
                time.sleep(5)
                
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

    def clean_html(self, html, base_url=""):
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
                html, err = BrowserDriver.fetch_html(url)
                if not html: return f"Error: {err}"
            else:
                resp.raise_for_status()
                html = resp.text
        except Exception as e:
            log(f"Requests failed: {e}. Invoking DrissionPage.")
            html, err = BrowserDriver.fetch_html(url)
            if not html: return f"Error: {err}"

        meta = self.extract_metadata(html)
        markdown = self.clean_html(html, base_url=url)
        
        return f"{meta}\n=== CONTENT ===\n{markdown}"

# ==========================================
# MAIN
# ==========================================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="URL")
    args = parser.parse_args()
    
    cp = ContentParser()
    result = cp.process_url(args.input)
    
    out = Config.get_output_path()
    try:
        with open(out, "w", encoding="utf-8") as f: f.write(result)
        log(f"Saved {len(result)} chars to {out}")
    except Exception as e:
        log(f"Save failed: {e}")

if __name__ == "__main__":
    main()

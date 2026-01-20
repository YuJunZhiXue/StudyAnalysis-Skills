import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
import tempfile

# Configuration
MAX_CHARS_DEFAULT = 50000  # Approx 12k-15k tokens
TRUNCATION_MSG = "\n\n[SYSTEM: CONTENT TRUNCATED DUE TO LENGTH LIMIT]"

def log(msg):
    print(f"[Ingester] {msg}")

def lazy_import_ocr():
    try:
        from rapidocr_onnxruntime import RapidOCR
        return RapidOCR()
    except ImportError:
        return None

def lazy_import_pdf():
    try:
        from pypdf import PdfReader
        return PdfReader
    except ImportError:
        return None

def is_valid_image(img_path):
    if os.path.getsize(img_path) < 5120: 
        return False
    return True

def extract_text_from_image(image_path):
    ocr_engine = lazy_import_ocr()
    if not ocr_engine:
        return "[SYSTEM: OCR Skipped. Install 'rapidocr_onnxruntime' to enable image text extraction.]"

    if not is_valid_image(image_path):
        return ""
    
    try:
        result, _ = ocr_engine(image_path)
        if result:
            text = "\n".join([line[1] for line in result])
            return f"\n\n[IMAGE OCR CONTENT]\n{text}\n[/IMAGE OCR CONTENT]\n"
        return ""
    except Exception as e:
        log(f"OCR Failed: {e}")
        return ""

def download_image(url, save_dir):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            filename = os.path.basename(url.split("?")[0])
            if not filename: filename = "temp_img.jpg"
            save_path = os.path.join(save_dir, filename)
            with open(save_path, "wb") as f:
                f.write(response.content)
            return save_path
    except Exception as e:
        log(f"Image download failed: {e}")
    return None

def process_url(url, max_chars):
    log(f"Processing URL: {url}")
    
    # Direct Image
    if url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        with tempfile.TemporaryDirectory() as temp_dir:
            img_path = download_image(url, temp_dir)
            if img_path:
                return extract_text_from_image(img_path)
            return ""

    # HTML
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Check Content-Length if available to fail fast on massive files
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 10 * 1024 * 1024: # 10MB limit
             return f"[SYSTEM: URL Content too large ({int(content_length)/1024/1024:.2f} MB). Skipped.]"

        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text_content = soup.get_text(separator='\n', strip=True)
        
        if len(text_content) > max_chars:
            return f"URL: {url}\n\n=== WEB TEXT ===\n{text_content[:max_chars]}{TRUNCATION_MSG}"

        # Extract Images (Only if text is not huge)
        img_ocr_content = ""
        images = soup.find_all('img')
        if images and len(text_content) < max_chars * 0.8: # Save space for OCR
            log(f"Found {len(images)} images. Scanning top 5...")
            with tempfile.TemporaryDirectory() as temp_dir:
                for i, img in enumerate(images[:5]): # Limit to top 5 images
                    src = img.get('src')
                    if not src: continue
                    if not src.startswith('http'):
                        if src.startswith('//'): src = 'https:' + src
                        elif src.startswith('/'): src = '/'.join(url.split('/')[:3]) + src
                        else: continue
                    
                    local_path = download_image(src, temp_dir)
                    if local_path:
                        ocr_text = extract_text_from_image(local_path)
                        if ocr_text:
                            img_ocr_content += ocr_text

        final_content = f"URL: {url}\n\n=== WEB TEXT ===\n{text_content}\n\n=== IMAGE CONTENT ===\n{img_ocr_content}"
        
        if len(final_content) > max_chars:
            return final_content[:max_chars] + TRUNCATION_MSG
            
        return final_content

    except Exception as e:
        return f"Error processing URL: {e}"

def process_local_file(path, max_chars):
    log(f"Processing Local File: {path}")
    if not os.path.exists(path):
        return "Error: File not found."
    
    file_size = os.path.getsize(path)
    if file_size > 10 * 1024 * 1024: # 10MB limit
        return "[SYSTEM: File too large (>10MB). Skipped to prevent memory overflow.]"

    if path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        return extract_text_from_image(path)
    
    if path.lower().endswith('.pdf'):
        PdfReader = lazy_import_pdf()
        if not PdfReader:
             return "[SYSTEM: PDF Skipped. Install 'pypdf' to enable PDF reading.]"
        try:
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
                if len(text) > max_chars:
                    return text[:max_chars] + TRUNCATION_MSG
            return text
        except Exception as e:
            return f"Error reading PDF: {e}"

    # Default text reading
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
            if len(text) > max_chars:
                return text[:max_chars] + TRUNCATION_MSG
            return text
    except Exception as e:
        return f"Error reading file: {e}"

def main():
    parser = argparse.ArgumentParser(description="Knowledge Absorber Content Ingester")
    parser.add_argument("input", help="URL or Local File Path")
    parser.add_argument("--max-chars", type=int, default=MAX_CHARS_DEFAULT, help="Max characters to capture")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_output = os.path.abspath(os.path.join(script_dir, "..", "config", "raw_content.txt"))
    
    parser.add_argument("--output", default=default_output, help="Output file path")
    
    args = parser.parse_args()
    
    result = ""
    if args.input.startswith("http"):
        result = process_url(args.input, args.max_chars)
    else:
        result = process_local_file(args.input, args.max_chars)
        
    # Ensure directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result)
        
    log(f"Extraction complete. Saved to {args.output} (Size: {len(result)} chars)")

if __name__ == "__main__":
    main()

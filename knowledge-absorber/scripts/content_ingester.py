import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from rapidocr_onnxruntime import RapidOCR
import tempfile

# Initialize OCR engine once
ocr_engine = RapidOCR()

def log(msg):
    print(f"[Ingester] {msg}")

def is_valid_image(img_path):
    # Simple check: File size > 5KB (Skip icons/tracking pixels)
    if os.path.getsize(img_path) < 5120: 
        return False
    return True

def extract_text_from_image(image_path):
    if not is_valid_image(image_path):
        log(f"Skipping small image: {image_path}")
        return ""
    
    try:
        result, _ = ocr_engine(image_path)
        if result:
            text = "\n".join([line[1] for line in result])
            return f"\n\n[IMAGE OCR CONTENT]\n{text}\n[/IMAGE OCR CONTENT]\n"
        return ""
    except Exception as e:
        log(f"OCR Failed for {image_path}: {e}")
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
        log(f"Failed to download image {url}: {e}")
    return None

def process_url(url):
    log(f"Processing URL: {url}")
    
    # Check if it's a direct image
    if url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        with tempfile.TemporaryDirectory() as temp_dir:
            img_path = download_image(url, temp_dir)
            if img_path:
                return extract_text_from_image(img_path)
            return ""

    # Assume HTML
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract main text
        text_content = soup.get_text(separator='\n', strip=True)
        
        # Extract Images
        img_ocr_content = ""
        images = soup.find_all('img')
        log(f"Found {len(images)} images in HTML.")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, img in enumerate(images):
                src = img.get('src')
                if not src: continue
                if not src.startswith('http'):
                    # Handle relative URLs (simplified)
                    if src.startswith('//'): src = 'https:' + src
                    elif src.startswith('/'): src = '/'.join(url.split('/')[:3]) + src
                    else: continue # Skip complex relative paths for now
                
                log(f"Checking image {i+1}/{len(images)}: {src}")
                local_path = download_image(src, temp_dir)
                if local_path:
                    ocr_text = extract_text_from_image(local_path)
                    if ocr_text:
                        img_ocr_content += ocr_text

        return f"URL: {url}\n\n=== WEB TEXT ===\n{text_content}\n\n=== IMAGE CONTENT ===\n{img_ocr_content}"

    except Exception as e:
        log(f"Error processing URL {url}: {e}")
        return ""

def process_local_file(path):
    log(f"Processing Local File: {path}")
    if not os.path.exists(path):
        return "Error: File not found."
    
    if path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        return extract_text_from_image(path)
    
    # PDF support (Basic placeholder - requires pypdf)
    if path.lower().endswith('.pdf'):
        try:
            from pypdf import PdfReader
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except ImportError:
            return "Error: pypdf not installed."
        except Exception as e:
            return f"Error reading PDF: {e}"

    return "Unsupported file type."

def main():
    parser = argparse.ArgumentParser(description="Knowledge Absorber Content Ingester")
    parser.add_argument("input", help="URL or Local File Path")
    parser.add_argument("--output", default="raw_content.txt", help="Output file path")
    
    args = parser.parse_args()
    
    result = ""
    if args.input.startswith("http"):
        result = process_url(args.input)
    else:
        result = process_local_file(args.input)
        
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(result)
        
    log(f"Extraction complete. Saved to {args.output}")

if __name__ == "__main__":
    main()

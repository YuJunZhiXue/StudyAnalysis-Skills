import os
import sys
import argparse
import time
import random
# DrissionPage and BeautifulSoup will be lazy imported to prevent crash on missing deps

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

def process_url_with_drission(url, max_chars):
    log(f"Attempting extraction with DrissionPage: {url}")
    try:
        co = ChromiumOptions()
        # 自动搜索常见浏览器路径
        browser_paths = [
            r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
            r'D:\Program Files\Google\Chrome\Application\chrome.exe',
            r'D:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
            r'D:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            r'D:\Program Files\Microsoft\Edge\Application\msedge.exe',
            # 360 浏览器路径
            r'C:\Users\Administrator\AppData\Local\360Chrome\Chrome\Application\360chrome.exe',
            r'D:\Users\Administrator\AppData\Local\360Chrome\Chrome\Application\360chrome.exe',
            r'C:\Program Files\360\360se6\Application\360se.exe',
            r'D:\Program Files\360\360se6\Application\360se.exe'
        ]
        
        target_path = None
        for path in browser_paths:
            if os.path.exists(path):
                target_path = path
                break
        
        if target_path:
            log(f"Using browser: {target_path}")
            co.set_browser_path(target_path)
            
            # 针对 CSDN: 用户反馈 VIP 功能已移除，使用默认逻辑
            # 使用标准 UA
            co.set_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        else:
            log("No common browser found, let DrissionPage search...")

        # 暂时关闭 headless 模式进行测试（如果环境允许）
        # co.set_argument('--headless') 
        co.set_argument('--no-sandbox')
        co.set_argument('--disable-gpu')
        # 移除可能引起冲突的参数
        # co.set_argument('--incognito') 
        
        try:
            page = ChromiumPage(co)
        except Exception as e:
            log(f"ChromiumPage init failed: {e}")
            # 尝试不指定路径，让 DrissionPage 自己找
            try:
                co2 = ChromiumOptions()
                co2.set_argument('--headless')
                page = ChromiumPage(co2)
            except:
                log("Fallback to SessionPage...")
                from DrissionPage import SessionPage
                page = SessionPage()
        
        try:
            page.get(url)
            
            # 处理知乎登录弹窗
            if "zhihu.com" in url:
                time.sleep(3)
                try:
                    # 尝试寻找并点击关闭登录弹窗的按钮 (通常是右上角的 X)
                    close_btn = page.ele('xpath://button[@aria-label="关闭"]')
                    if close_btn:
                        close_btn.click()
                        log("Closed Zhihu login modal.")
                except:
                    pass
                
                # 即使没关掉，尝试强制滚动，有些弹窗不影响底层内容读取
                page.scroll.to_bottom()
                time.sleep(1)
            
            if hasattr(page, 'html'):
                html = page.html
            else:
                html = page.response.text
            if "安全验证" in html or "验证码" in html:
                log("Anti-bot detected (Captcha).")
                return None

            soup = BeautifulSoup(html, 'html.parser')
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # CSDN 专属精确提取
            if "blog.csdn.net" in url:
                article = soup.find(id="content_views") or soup.find(id="article_content")
                if article:
                    # 再次清理内部可能的残留
                    for tag in article.find_all(class_=["recommend-box", "template-box", "hide-article-box", "signin", "login-mark"]):
                        tag.decompose()
                    clean_text = article.get_text(separator='\n', strip=True)
                    return f"[CSDN VIP MODE]\n{clean_text}"

            clean_text = soup.get_text(separator='\n', strip=True)
            return clean_text
        finally:
            page.quit()
    except Exception as e:
        log(f"DrissionPage failed: {e}")
        return None

def process_url_with_requests(url, max_chars):
    log("Attempting standard requests extraction...")
    try:
        import requests
        from bs4 import BeautifulSoup
        import time
        import random
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
        }
        
        time.sleep(random.uniform(1, 2))
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code == 403:
            log("Received 403, retrying with specialized headers and mobile simulation...")
            headers.update({
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                'Referer': 'https://www.google.com/',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            })
            time.sleep(random.uniform(2, 4))
            try:
                session = requests.Session()
                session.get("https://www.zhihu.com/", headers={'User-Agent': headers['User-Agent']}, timeout=10)
                response = session.get(url, headers=headers, timeout=15, allow_redirects=True)
                
                if response.status_code == 403:
                    clean_headers = {
                        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
                    }
                    time.sleep(random.uniform(1, 2))
                    response = requests.get(url, headers=clean_headers, timeout=15, allow_redirects=True)
            except Exception as e:
                log(f"Retry failed: {e}")

        if response.status_code == 403:
            log("Requests 403 persisted.")
            return None
            
        response.raise_for_status()
        
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 10 * 1024 * 1024: 
             return f"[SYSTEM: URL Content too large ({int(content_length)/1024/1024:.2f} MB). Skipped.]"

        soup = BeautifulSoup(response.content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()

        text_content = soup.get_text(separator='\n', strip=True)
        
        if len(text_content) < 500 and ("安全验证" in text_content or "验证码" in text_content):
            log("Anti-bot text detected in requests response.")
            return None
            
        if len(text_content) < 200:
            log("Requests content too short, suspecting incomplete load.")
            return None

        img_ocr_content = ""
        images = soup.find_all('img')
        if images and len(text_content) < max_chars * 0.8:
            log(f"Found {len(images)} images. Scanning top 5...")
            with tempfile.TemporaryDirectory() as temp_dir:
                for i, img in enumerate(images[:5]):
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
        return final_content

    except Exception as e:
        log(f"Requests logic failed: {e}")
        return None

def process_url(url, max_chars):
    log(f"Processing URL: {url}")

    # Image Check
    if url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        with tempfile.TemporaryDirectory() as temp_dir:
            img_path = download_image(url, temp_dir)
            if img_path:
                return extract_text_from_image(img_path)
            return ""

    # Priority 1: Standard Requests
    req_content = process_url_with_requests(url, max_chars)
    if req_content:
        log("Standard requests successful.")
        if len(req_content) > max_chars:
             return f"{req_content[:max_chars]}{TRUNCATION_MSG}"
        return req_content

    log("Standard requests failed/blocked. Switching to DrissionPage (Priority 2)...")
    
    # Priority 2: DrissionPage
    drission_content = process_url_with_drission(url, max_chars)
    if drission_content:
        log("DrissionPage extraction successful.")
        if len(drission_content) > max_chars:
            return f"URL: {url}\n\n=== WEB TEXT ===\n{drission_content[:max_chars]}{TRUNCATION_MSG}"
        return f"URL: {url}\n\n=== WEB TEXT ===\n{drission_content}"

    return "Error: All automatic extraction methods failed."

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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse
from time import sleep
import base64
import os
import re

import logging

# Suppress logs from the webdriver and chromedriver
logging.getLogger('selenium.webdriver').setLevel(logging.ERROR)
logging.getLogger('chromedriver').setLevel(logging.ERROR)

class Driver(webdriver.Chrome):
    def __init__(self, headless=False, debug=False):

        service = Service()
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if not debug:
            options.add_argument('--disable-logging')
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

        super().__init__(service=service, options=options)

        self.set_window_position(-6000, 0)
        self.implicitly_wait(3)

class Manwa:
    def __init__(self):
        self.website = ['manwa.me']
        self.driver = Driver(headless=False)

    def is_responsible(self, url):
        parsed_url = urlparse(url)
        for site in self.website:
            if parsed_url.netloc == site:
                return True
        return False
    
    def download_comic(self, url, folder):
        self.driver.get(url)

        sleep(1)

        book_name = self.driver.find_element(By.CLASS_NAME, "view-fix-top-bar-center-right-book-name").text.strip()
        chapter_name = self.driver.find_element(By.CLASS_NAME, "view-fix-top-bar-center-right-chapter-name").text.strip()

        comic_names = [book_name, chapter_name]

        savepath = folder
        illegal_chars = r'[<>:"/\\|?*]'
        for comic_name in comic_names:
            subfolder = re.sub(illegal_chars, ' ', comic_name)
            savepath = os.path.join(savepath, subfolder)
            
        print("-".join(comic_names))
        os.makedirs(savepath, exist_ok=True)

        img_tags = self.driver.find_elements(By.CLASS_NAME, "lazy_img")
        print(f"[INFO] Found {len(img_tags)} images.")

        for idx, img in enumerate(img_tags):
            self.driver.execute_script("arguments[0].scrollIntoView(true);", img) # 滾動到圖片位置確保它加載完成

            sleep(1) 

            # 使用 JavaScript 從 blob URL 提取圖片數據
            script = """
                var img = arguments[0];
                var canvas = document.createElement('canvas');
                canvas.width = img.naturalWidth;
                canvas.height = img.naturalHeight;
                var ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0);
                return canvas.toDataURL('image/png');  // 返回 Base64
            """
            img_data = self.driver.execute_script(script, img)

            file_name = os.path.join(savepath, f"{idx+1}.png")

            # 解碼 Base64 並保存圖片
            if img_data.startswith("data:image"):
                img_data = img_data.split(",")[1]
                img_bytes = base64.b64decode(img_data)

                with open(file_name, "wb") as f:
                    f.write(img_bytes)

                print(f"[INFO] Download succeeded: {file_name}")
            else:
                print(f"[ERROR] Download failed: {file_name}")

            sleep(1)

    def get_urls_from_page(self, url):
        self.driver.get(url)
        sleep(1)

        try:
            a_tag = self.driver.find_elements(By.CLASS_NAME, "chapteritem")
            links = [a.get_attribute("href") for a in a_tag if a.get_attribute("href")]
        except Exception as e:
            print(f"[ERROR] get_urls_from_page({url}): {e}")
        
        return links
    
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
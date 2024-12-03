from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote, urlparse
from time import sleep
import requests
import os
import re

class JComic:
    def __init__(self):
        self.website = ['jcomic.net']
    
    def is_responsible(self, url):
        parsed_url = urlparse(url)
        for site in self.website:
            if parsed_url.netloc == site:
                return True
        return False

    def get_urls_from_page(self, url):
        response = requests.get(url)
        parsed_url = urlparse(url)
        host = f"{parsed_url.scheme}://{parsed_url.netloc}"

        if response.status_code != 200:
            print(f"[ERROR] {url} with status code {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        links = [host+a['href'] for a in soup.find_all('a', href=re.compile(r'^/page/'))]
        return links

    
    def download_comic(self, url, folder):
        comic_names = re.sub(r'.*?jcomic\.net/page/', '', unquote(url)).split('/')
        
        savepath = folder

        illegal_chars = r'[<>:"/\\|?*]'
        for comic_name in comic_names:
            subfolder = re.sub(illegal_chars, '', comic_name)
            savepath = os.path.join(savepath, subfolder)
            
        print("-".join(comic_names))
        os.makedirs(savepath, exist_ok=True)

        response = requests.get(url)
        if response.status_code != 200:
            print(f"[ERROR] {url} with status code {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        img_tags = soup.find_all('img')
        print(f"[INFO] Found {len(img_tags)} images.")

        for img_tag in img_tags:
            img_url = img_tag.get('src')
            if not img_url:
                continue

            # 解析完整的圖片 URL
            img_url = urljoin(url, img_url)

            # 過濾掉不包含 "X-Amz-" 的 URL（確認是否為簽名 URL）
            if "X-Amz-" not in img_url:
                continue

            # 下載圖片
            try:
                img_data = requests.get(img_url).content
                file_name = os.path.join(savepath, unquote(os.path.basename(img_url.split('?')[0])))  # 去掉參數保存乾淨檔名
                with open(file_name, 'wb') as file:
                    file.write(img_data)
                print(f"[INFO] Download succeeded: {file_name}")
            except Exception as e:
                print(f"[ERROR] Download failed: {file_name} {e}")
            
            sleep(1)
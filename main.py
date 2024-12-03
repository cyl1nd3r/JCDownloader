from jcomic import JComic
from manwa import Manwa
from utils import get_urls_from_file
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--savedir', type=str, help="the dir to save the imgs", default='images')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=str, help="url list from file")
    group.add_argument('--urls', type=str, help="url list from jcomic url")
    group.add_argument('--url', type=str, help="url")
    args = parser.parse_args()
    
    apps = [JComic(), Manwa()]

    urls = []
    if args.file:
        # 如果 --file 被提供，則從文件中獲取 URL
        get_urls_from_file(args.file)
    elif args.url:
        urls = [args.url]
    elif args.urls:
        # 如果 --urls 被提供，則從 URL 中獲取 URL
        for app in apps:
            if app.is_responsible(args.urls):
                urls = app.get_urls_from_page(args.urls)
                break
    
    savedir = args.savedir

    for url in urls:
        for app in apps:
            if app.is_responsible(url):
                app.download_comic(url, savedir)
                break

if __name__ == "__main__":
    main()
# JC Downloader

This CLI program allows you to download comic images from a specified URL or a list of URLs. You can either provide a list of URLs from a file or directly from a JComic `https://jcomic.net/author/XXX` URL. The script will download the comic images and save them in a specified directory.

## Disclaimer

**Please be aware that downloading or distributing comics from unofficial or unauthorized sources, such as JComic sites, may be illegal in your country. We do not encourage or endorse the use of this script for illegal activities. This script is for educational purposes only. Always ensure that you have the proper rights and permissions before downloading any content.**

## Supported Websites

- `jcomic.net`
- `manwa.me`

## Requirements

- Python 3
- Required libraries:
  - `requests`: To make HTTP requests and download images.
  - `BeautifulSoup` from `bs4`: To parse HTML and extract image links.
  - `selenium`: To crawl websites that are hard to fetch by `requests`.

You can install the required libraries using `pip`:

```bash
pip install requests beautifulsoup4 selenium
```

## Usage

### Command-line Arguments

1. **`--file`**: Path to a file containing a list of URLs (each line contains one url) to download comics from.
2. **`--urls`**: URL to a webpage containing links to comic pages:
   - `JComic`: `https://jcomic.net/author/XXX` or `https://jcomic.net/eps/XXX`
   - `Manwa`: `https://manwa.me/book/XXX`
3. **`--url`**: A single URL from which to download comic images:
   - `JComic`: `https://jcomic.net/page/XXX`
   - `Manwa`: `https://manwa.me/chapter/XXX`
4. **`--savedir`**: Directory to save downloaded images. Default is `images`.

### Example Commands

1. **Download comics from a file containing URLs:**

```bash
python main.py --file urls.txt
```

2. **Download comics from a single URL:**

```bash
python main.py --url https://jcomic.net/page/XXX
```

3. **Download comics from a URL that contains links to pages (e.g., JComic URL):**

```bash
python main.py --urls https://jcomic.net/author/XXX
```

### How it works

1. **Download Images:**
   - The script will extract all the `<img>` tags from the specified URL(s).
   - It downloads each image and saves it into a folder based on the comic name, ensuring the folder name is sanitized to avoid illegal characters.

2. **Fetching URLs:**
   - You can provide a list of URLs through a file or directly from a webpage URL. 
   - If the list is from a file (`--file`), it reads the file line by line.
   - If the list is from a URL (`--urls`), it extracts all URLs that match the pattern `/page/xxx`.

3. **Saving Images:**
   - Images are saved in the specified directory, with each comic's images being stored in a subfolder named after the comic.

## Example Output

```plaintext
[INFO] Find 10 images.
[INFO] Download succeeded: images/comic1/1.jpg
[INFO] Download succeeded: images/comic1/2.jpg
...
```

## License

This script is free to use and modify under the MIT License.
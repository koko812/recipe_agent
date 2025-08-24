# collect_urls.py
import requests, json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

START = "https://publicdomainrecipes.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (crawler-demo)"}

def fetch(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    return r.url, r.status_code, r.text  # ← 最終URLも返る

def collect_children(start: str, limit: int | None = None):

    root_final, code, html = fetch(start)
    host = urlparse(root_final).netloc
    soup = BeautifulSoup(html, "html.parser")

    seen, out = set(), []
    for a in soup.select("a[href]"):
        u = urljoin(root_final, a["href"]).rstrip("/")
        if urlparse(u).netloc == host and u not in seen:
            seen.add(u)
            out.append({"url": u})
            if limit and len(out) >= limit:
                break
    return out

if __name__ == "__main__":
    urls = collect_children(START, limit=10)
    print(json.dumps(urls, ensure_ascii=False, indent=2))


# inspect_page.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import Counter

URL = "https://publicdomainrecipes.com/"  # さっきのURLに差し替え

headers = {"User-Agent": "Mozilla/5.0 (crawler-demo)"}  # 簡易UA
resp = requests.get(URL, headers=headers, timeout=20)
print("status:", resp.status_code)
print("final_url:", resp.url)

soup = BeautifulSoup(resp.text, "html.parser")

# タイトル
title = soup.title.string.strip() if soup.title and soup.title.string else "(no title)"
print("\n[TITLE]\n", title)

# 見出しアウトライン（最初の数件だけ）
def texts(els, limit=10):
    return [e.get_text(strip=True) for e in els[:limit]]

print("\n[HEADINGS]")
for tag in ["h1", "h2", "h3"]:
    hs = texts(soup.select(tag), 10)
    print(f" {tag}: {len(hs)} ->", hs)

# リンク一覧とドメイン分布
links = []
for a in soup.find_all("a", href=True):
    absurl = urljoin(resp.url, a["href"])
    links.append(absurl)

hosts = [urlparse(u).netloc for u in links]
print("\n[LINKS]")
print(" total:", len(links))
print(" unique hosts (top5):", Counter(hosts).most_common(5))


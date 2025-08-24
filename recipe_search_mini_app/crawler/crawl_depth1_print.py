# crawl_depth1.py
import requests, time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

START = "https://publicdomainrecipes.com/"  # 起点URLに差し替え
headers = {"User-Agent": "Mozilla/5.0 (crawler-demo)"}

def fetch(url):
    r = requests.get(url, headers=headers, timeout=20)
    return r.url, r.status_code, r.text

root_final, code, html = fetch(START)
print("ROOT:", root_final, code)

root_host = urlparse(root_final).netloc
soup = BeautifulSoup(html, "html.parser")

# 同一ドメインのリンクだけ
childs = []
for a in soup.select("a[href]"):
    u = urljoin(root_final, a["href"])
    if urlparse(u).netloc == root_host:
        childs.append(u)

# 重複を削って上位だけ
seen = set()
uniq = []
for u in childs:
    if u not in seen:
        seen.add(u)
        uniq.append(u)
childs = uniq[:10]

print("\nCHILD PAGES (same host, up to 10):")
for u in childs:
    time.sleep(0.5)  # 優しめに
    final, c, h = fetch(u)
    soup2 = BeautifulSoup(h, "html.parser")
    title = soup2.title.string.strip() if soup2.title and soup2.title.string else "(no title)"
    print(f"- {final} [{c}] {title}")

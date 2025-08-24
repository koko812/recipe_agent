# probe_site.py
import requests, re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def probe(url: str):
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")
    host = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(r.url))

    # robots / sitemap
    robots = requests.get(urljoin(host, "/robots.txt")).status_code
    sm = requests.get(urljoin(host, "/sitemap.xml")).status_code

    # 見出し数とリスト構造
    h1 = len(soup.select("h1")); h2 = len(soup.select("h2"))
    uls = len(soup.select("ul li")); ols = len(soup.select("ol li"))

    # JSON-LD（schema.org/Recipe）有無
    has_jsonld = any("application/ld+json" in (s.get("type") or "")
                     and "Recipe" in s.get_text()
                     for s in soup.find_all("script"))

    print(f"final_url: {r.url}")
    print(f"robots.txt: {robots}, sitemap.xml: {sm}")
    print(f"h1={h1}, h2={h2}, ul-li={uls}, ol-li={ols}, json-ld={has_jsonld}")

if __name__ == "__main__":
    probe("https://publicdomainrecipes.com/basic-waffles/")


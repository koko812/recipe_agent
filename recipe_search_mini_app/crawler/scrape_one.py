# scrape_one.py
import re
import requests
from bs4 import BeautifulSoup

def minutes_from_text(s: str) -> int | None:
    # "10 mins", "20 min", "1 hr 10 mins" など簡易パース（雑に対応）
    s = s.lower()
    mins = 0
    found = False
    # 時間
    m = re.search(r'(\d+)\s*hour|\b(\d+)\s*hr', s)
    if m:
        h = int(m.group(1) or m.group(2))
        mins += 60 * h
        found = True
    # 分
    for m in re.finditer(r'(\d+)\s*mins?|\b(\d+)\s*min\b', s):
        v = int(m.group(1) or m.group(2))
        mins += v
        found = True
    return mins if found else None

def scrape_publicdomainrecipes(url: str):
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # タイトル（<h1>）
    title = soup.select_one("h1")
    title = title.get_text(strip=True) if title else "(no title)"

    # ページ先頭のメタ行（Prep/Cook/Amount）をテキスト抽出
    meta_text = soup.get_text("\n", strip=True)
    prep = re.search(r'Prep time:\s*([^\n]+)', meta_text)
    cook = re.search(r'Cook time:\s*([^\n]+)', meta_text)
    total_time = 0
    cnt = 0
    for mm in [prep.group(1) if prep else None, cook.group(1) if cook else None]:
        if mm:
            mval = minutes_from_text(mm)
            if mval is not None:
                total_time += mval
                cnt += 1
    total_time_min = total_time if cnt > 0 else None

    # Ingredients セクション（見出し “Ingredients” の直後の <ul>）
    ing_ul = None
    for h in soup.select("h2, h3"):
        if h.get_text(strip=True).lower().startswith("ingredients"):
            sib = h.find_next_sibling()
            while sib and sib.name not in ("ul", "ol"):
                sib = sib.find_next_sibling()
            ing_ul = sib if sib and sib.name == "ul" else None
            break
    ingredients = []
    if ing_ul:
        for li in ing_ul.select("li"):
            txt = li.get_text(" ", strip=True)
            ingredients.append(txt)

    # Directions セクション（見出し “Directions” の直後の <ol>）
    steps_ol = None
    for h in soup.select("h2, h3"):
        if h.get_text(strip=True).lower().startswith("directions"):
            sib = h.find_next_sibling()
            while sib and sib.name not in ("ul", "ol"):
                sib = sib.find_next_sibling()
            steps_ol = sib if sib and sib.name == "ol" else None
            break
    directions = []
    if steps_ol:
        for li in steps_ol.select("li"):
            directions.append(li.get_text(" ", strip=True))

    return {
        "title": title,
        "url": resp.url,
        "total_time_min": total_time_min,
        "ingredients_raw": ingredients,
        "directions_raw": directions,
    }

if __name__ == "__main__":
    data = scrape_publicdomainrecipes("https://publicdomainrecipes.com/basic-waffles/")
    from pprint import pprint
    pprint(data)


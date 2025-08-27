# extract_pr_name.py
import requests
from bs4 import BeautifulSoup

def fetch_pr_names(url):
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = BeautifulSoup(r.text, "lxml")
    # class="pr_name" の td からテキスト抽出
    names = [td.get_text(" ", strip=True) for td in soup.find_all("td", class_="pr_name")]
    return names

def filter_fatty_acids(names):
    drop_heads = {"総量", "飽和", "一価不飽和", "多価不飽和", "n-3系 多価不飽和", "n-6系 多価不飽和"}
    out = []
    for n in names:
        if n in drop_heads:
            continue
        if n and n[0].isdigit():  # 数字から始まる
            continue
        out.append(n)
    return out


if __name__ == "__main__":
    base = "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10142_7&MODE="
    fa_raw = fetch_pr_names(base+"4")  # MODE=4
    fa_clean = filter_fatty_acids(fa_raw)
    print("=== アミノ酸 (MODE=1) ===")

    for n in fetch_pr_names(base+"1"):
        print("-", n)

    print("\n=== 脂肪酸 cleaned ===")
    for n in fa_clean:
        print("-", n)

    print("\n=== 炭水化物 (MODE=7) ===")
    for n in fetch_pr_names(base+"7"):
        print("-", n)

    print("\n=== 炭水化物 (MODE=9) ===")
    for n in fetch_pr_names(base+"9"):
        print("-", n)


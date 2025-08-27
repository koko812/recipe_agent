# crawl_mext_page.py
# 使い方:
#   uv run crawl_mext_page.py "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10142_7&MODE=0"
# 出力:
#   - 見つかった h1 / h2 を標準出力
#   - 見つかったリンク(a[href])を上位20件だけ表示
#   - テーブル件数と各テーブルの行数
#   - タグ出現数トップ20
#   - tables/table_*.csv に表をCSV保存（必要あれば）

import sys, os, time, csv
from collections import Counter
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

def fetch(url, timeout=15, retries=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; mext-crawler/0.1; +https://example.org)",
        "Accept-Language": "ja,en;q=0.8",
    }
    for i in range(retries+1):
        try:
            r = requests.get(url, headers=headers, timeout=timeout)
            r.raise_for_status()
            # 文字化け対策：サーバ指定 > apparent_encoding
            if not r.encoding or r.encoding.lower() in ("iso-8859-1", "ascii"):
                r.encoding = r.apparent_encoding
            return r.text
        except Exception as e:
            if i == retries:
                raise
            time.sleep(1.0 + i)

def parse_tables(soup):
    tables = []
    for ti, tbl in enumerate(soup.find_all("table")):
        rows = []
        for tr in tbl.find_all("tr"):
            cells = [c.get_text(strip=True) for c in tr.find_all(["th","td"])]
            if cells:
                rows.append(cells)
        if rows:
            tables.append(rows)
    return tables

def save_tables_csv(tables, outdir="tables"):
    os.makedirs(outdir, exist_ok=True)
    for i, rows in enumerate(tables, start=1):
        path = os.path.join(outdir, f"table_{i}.csv")
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for row in rows:
                w.writerow(row)

# 追加関数：そのままの table HTML をファイル保存
def save_table_htmls(soup, url, outdir="tables_html"):
    import os
    from urllib.parse import urlparse

    os.makedirs(outdir, exist_ok=True)

    # <base> を入れて相対リンクが生きるようにしておく
    base_tag = f'<base href="{url}">\n'

    for i, tbl in enumerate(soup.find_all("table"), start=1):
        # outerHTML をそのまま取りたいので、.prettify() ではなく str(tbl)
        html = "<!doctype html>\n<html><head>" + base_tag + "</head><body>\n" + str(tbl) + "\n</body></html>"
        path = os.path.join(outdir, f"table_{i}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10142_7&MODE=0"
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")

    # …（既存の解析や表示はそのまま）…

    # ★ テーブルの“元HTML”を保存（構造解析用）
    save_table_htmls(soup, url)

    # 参考：どのテーブルが何行あるかだけ軽く表示
    tables = parse_tables(soup)
    print(f"\n=== Tables ===")
    print("tables found:", len(tables))
    for i, rows in enumerate(tables, start=1):
        print(f"  table_{i}: {len(rows)} rows  (HTML: tables_html/table_{i}.html)")


if __name__ == "__main__":
    main()


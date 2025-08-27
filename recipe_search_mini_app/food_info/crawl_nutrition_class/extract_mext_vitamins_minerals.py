# extract_mext_vitamins_minerals.py
# 使い方:
#   uv run extract_mext_vitamins_minerals.py "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10142_7&MODE=0"
# 出力:
#   vitamins_minerals.csv（section,name,value,unit）
#   標準出力に上位数行をプレビュー

import re, sys, csv, time, os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

TARGET_SECTIONS = {"無機質", "ビタミン"}

def fetch(url, timeout=15, retries=2):
    ua = "Mozilla/5.0 (compatible; mext-scraper/0.1)"
    for i in range(retries + 1):
        try:
            r = requests.get(url, headers={"User-Agent": ua})
            r.raise_for_status()
            if not r.encoding or r.encoding.lower() in ("iso-8859-1", "ascii"):
                r.encoding = r.apparent_encoding
            return r.text
        except Exception:
            if i == retries:
                raise
            time.sleep(1 + i)

def abbr_text(cell):
    ab = cell.find("abbr")
    if ab and ab.has_attr("title"):
        return ab["title"].strip()
    return cell.get_text(" ", strip=True)

def expand_table_to_grid(table):
    grid = []
    r = 0
    for tr in table.find_all("tr"):  # thead/tbody も含めて取得
        c = 0
        if len(grid) <= r: grid.append([])
        cells = tr.find_all(["th", "td"])
        for cell in cells:
            txt = abbr_text(cell)
            cs = int(cell.get("colspan", 1))
            rs = int(cell.get("rowspan", 1))
            # 次の空き列を探す
            while True:
                if len(grid[r]) <= c: grid[r].append("")
                if grid[r][c] == "":
                    break
                c += 1
            # 配置
            for j in range(cs):
                if len(grid[r]) <= c + j:
                    grid[r] += [""] * (c + j - len(grid[r]) + 1)
                grid[r][c + j] = txt
            # 下行の占有マーク
            for dr in range(1, rs):
                rr = r + dr
                while len(grid) <= rr:
                    grid.append([])
                while len(grid[rr]) < c + cs:
                    grid[rr].append("")
                for j in range(cs):
                    if grid[rr][c + j] == "":
                        grid[rr][c + j] = "<SPAN>"
            c += cs
        r += 1
    # 後処理
    maxw = max((len(row) for row in grid), default=0)
    for row in grid:
        for i, v in enumerate(row):
            if v == "<SPAN>":
                row[i] = ""
        if len(row) < maxw:
            row += [""] * (maxw - len(row))
    return grid

NUM_RE = re.compile(r"^[-−(]?\d+(\.\d+)?\)?$")  # 例: 0, 16.9, (0.4)
UNIT_CAND = {"g","mg","µg","μg","kcal","kJ","%"}  # 必要に応じて追加

def choose_columns(grid):
    """
    ざっくり:
      - 右端2列を 値/単位 とみなす（多くのページで一致）
      - 左のどこかにセクション（無機質/ビタミン等）が立っている
      - 残りを name とする
    """
    if not grid: return None
    width = len(grid[0])
    val_col = width - 2
    unit_col = width - 1
    # セクションは左側の列に出やすいので候補を先頭3列から
    section_cols = list(range(min(3, width)))
    return section_cols, val_col, unit_col

def forward_fill(sections, row):
    # 左から最初に非空のものをセクションに採用（縦見出しのFFill）
    for col in sections:
        if row[col].strip():
            return row[col].strip()
    return None

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "https://fooddb.mext.go.jp/details/details.pl?ITEM_NO=10_10142_7&MODE=0"
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", {"id": "nut"}) or soup.find("table")
    grid = expand_table_to_grid(table)

    section_cols, val_col, unit_col = choose_columns(grid)

    out_rows = []
    last_section = None
    for row in grid:
        # セクション更新
        sec = forward_fill(section_cols, row) or last_section
        if sec: last_section = sec

        # 行が「成分名 値 単位」に見えるかのゆる判定
        val = row[val_col].strip() if val_col < len(row) else ""
        unit = row[unit_col].strip() if unit_col < len(row) else ""
        name_candidates = [x for i,x in enumerate(row[:-2]) if x.strip()]
        name = name_candidates[-1].strip() if name_candidates else ""

        # 抽出条件
        if sec in TARGET_SECTIONS and name and (val or unit):
            # 単位が abbr→title で展開されているので UNIT_CAND でざっくり確認
            if (val and (NUM_RE.match(val) or val in {"-", "Tr", "tr"})) or (unit in UNIT_CAND):
                out_rows.append((sec, name, val, unit))

    # 保存＆プレビュー
    os.makedirs("out", exist_ok=True)
    path = "out/vitamins_minerals.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["section", "name", "value", "unit"])
        w.writerows(out_rows)

    print(f"rows: {len(out_rows)} -> {path}")
    for r in out_rows[:12]:
        print(r)

if __name__ == "__main__":
    main()


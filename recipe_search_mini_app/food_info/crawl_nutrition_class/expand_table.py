# expand_table.py（短め・置き換え版）
from bs4 import BeautifulSoup
import sys

def expand_table_to_grid(table):
    grid = []  # 2D: list[list[str]]

    def ensure_size(r, cmax):
        while len(grid) <= r:
            grid.append([])
        if len(grid[r]) < cmax:
            grid[r] += [""] * (cmax - len(grid[r]))

    r = 0
    for tr in table.find_all("tr"):  # ネストあり
        # 次に詰める列位置を探すため、既存の予約（占有）も含め行の長さを見ながらスキャン
        c = 0
        ensure_size(r, 0)
        cells = tr.find_all(["th", "td"])  # ネストあり

        # 1セルずつ配置
        for cell in cells:
            text = cell.get_text(" ", strip=True)
            # <abbr title="...">があれば優先
            ab = cell.find("abbr")
            if ab and ab.has_attr("title"):
                text = ab["title"]

            cs = int(cell.get("colspan", 1))
            rs = int(cell.get("rowspan", 1))

            # 次の空き列 c を探す（空文字 "" が“未配置”の印）
            while True:
                ensure_size(r, c+1)
                if grid[r][c] == "":
                    break
                c += 1

            # 配置：この行に colspan 分テキストを置く
            ensure_size(r, c+cs)
            for j in range(cs):
                grid[r][c+j] = text

            # 下の行（rowspan-1 行）に予約を入れる（占有マークとして特殊トークンを入れる）
            for dr in range(1, rs):
                ensure_size(r+dr, c+cs)
                for j in range(cs):
                    # まだ空いてるところだけ占有マーク
                    if grid[r+dr][c+j] == "":
                        grid[r+dr][c+j] = "<SPAN>"

            # 次セルは少なくとも右隣へ
            c += cs

        r += 1

    # 占有マークを空に戻し、列幅を揃える
    maxw = max((len(row) for row in grid), default=0)
    for row in grid:
        for i, v in enumerate(row):
            if v == "<SPAN>":
                row[i] = ""
        if len(row) < maxw:
            row += [""] * (maxw - len(row))
    return grid

if __name__ == "__main__":
    html_path = sys.argv[1]
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")
    table = soup.find("table")  # id="nut" でもOK
    grid = expand_table_to_grid(table)

    # 先頭20行だけ表示
    for i, row in enumerate(grid[:20], 1):
        print(f"{i:02d} | " + " | ".join(row))


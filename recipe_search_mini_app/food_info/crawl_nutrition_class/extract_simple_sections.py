# extract_sections_from_comments.py
from bs4 import BeautifulSoup, Comment

def extract_sections(path):
    with open(path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "lxml")

    comments = [c.strip() for c in soup.find_all(string=lambda t: isinstance(t, Comment))]

    # コメントのリストから欲しい区間を切り出す
    minerals = []
    vitamins = []

    try:
        i1 = comments.index("無機質")
        i2 = comments.index("ビタミン")
        i3 = comments.index("アルコール")
    except ValueError as e:
        print("Expected section comments not found:", e)
        return minerals, vitamins

    # 無機質〜ビタミン
    minerals = comments[i1+1:i2]

    # ビタミン〜アルコール
    vitamins = comments[i2+1:i3]

    return minerals, vitamins

if __name__ == "__main__":
    minerals, vitamins = extract_sections("tables_html/table_2.html")
    print("=== 無機質 ===")
    for m in minerals:
        print("-", m)
    print("\n=== ビタミン ===")
    for v in vitamins:
        print("-", v)


from bs4 import BeautifulSoup

with open("tables_html/table_2.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

def walk(el, depth=0):
    indent = "  " * depth
    if el.name in ("tr","td","th"):
        # テキストと属性を簡潔に
        text = el.get_text(" ", strip=True)
        text = (text[:20] + "...") if len(text) > 20 else text
        attrs = []
        for a in ("colspan","rowspan","class"):
            if el.has_attr(a):
                attrs.append(f"{a}={el[a]}")
        attr_str = " ".join(attrs)
        print(f"{indent}<{el.name} {attr_str}> {text}")
    # 子要素を探索
    for child in el.find_all(recursive=False):
        walk(child, depth+1)

table = soup.find("table", {"id":"nut"})
walk(table)


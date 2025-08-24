import requests
from bs4 import BeautifulSoup

url = "https://www.federalregister.gov/public-inspection"  # ← 実際は Public Domain Recipes のURLに置き換え
resp = requests.get(url)
print(resp.status_code)  # 200 が返ればOK
print(resp.text[:500])   # ページの先頭500文字を表示

soup = BeautifulSoup(resp.text, "html.parser")

# 例えばレシピタイトルを h2 タグから取るとき
titles = [h2.get_text() for h2 in soup.find_all("h2")]
print(titles[:10])


# fdc_get_one.py
import os, requests
API_KEY = os.environ["FDC_API_KEY"]
BASE = "https://api.nal.usda.gov/fdc/v1"

fdc_id = 170932  # 上の検索結果で拾ったIDを入れる
r = requests.get(f"{BASE}/food/{fdc_id}", params={"api_key": API_KEY}, timeout=20)
r.raise_for_status()
data = r.json()
print(data["description"])
# 必要なら data["foodNutrients"] から栄養、data["foodCategory"] などを利用


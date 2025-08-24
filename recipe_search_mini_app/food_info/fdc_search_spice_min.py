# fdc_search_spice_min.py
import os, requests

API_KEY = os.environ["FDC_API_KEY"]  # 事前に輸入：export FDC_API_KEY="..."
BASE = "https://api.nal.usda.gov/fdc/v1"

def search_spice(q: str, page_size: int = 5):
    # /foods/search は GET でも POST でも可。まずは GET で簡単に。
    params = {"api_key": API_KEY, "query": q, "pageSize": page_size, "dataType": ["Foundation", "SR Legacy"]}
    r = requests.get(f"{BASE}/foods/search", params=params, timeout=20)
    r.raise_for_status()
    for f in r.json().get("foods", []):
        print(f"- {f.get('description')}  (fdcId={f.get('fdcId')}, dataType={f.get('dataType')})")

if __name__ == "__main__":
    # 例：クミン・ターメリック・サフラン
    for term in ["cumin", "turmeric", "saffron"]:
        print(f"\n### {term}")
        search_spice(term)


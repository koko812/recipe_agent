# fdc_show_nutrients.py
import os, sys, requests

API_KEY = os.environ["FDC_API_KEY"]
BASE = "https://api.nal.usda.gov/fdc/v1"

def show_food(fdc_id: int):
    r = requests.get(f"{BASE}/food/{fdc_id}", params={"api_key": API_KEY}, timeout=20)
    r.raise_for_status()
    data = r.json()

    print(f"Name: {data.get('description')}")
    cat = (data.get('foodCategory') or {}).get('description')
    print(f"Category: {cat}")

    # 栄養は dataType によって 'value' or 'amount' のどちらかなので両方対応
    nutrients = []
    for n in data.get("foodNutrients", []):
        name = n.get("nutrientName") or (n.get("nutrient") or {}).get("name")
        unit = n.get("unitName") or (n.get("nutrient") or {}).get("unitName")
        val  = n.get("value")
        if val is None:
            val = n.get("amount")
        if name and unit and val is not None:
            nutrients.append((name, val, unit))

    # 代表的な項目だけ先に出す（あれば）
    pick = {"Energy","Protein","Total lipid (fat)","Carbohydrate, by difference",
            "Sugars, total including NLEA","Fiber, total dietary","Sodium, Na"}
    picked = [x for x in nutrients if x[0] in pick]
    if picked:
        print("\nKey nutrients:")
        for name, val, unit in picked:
            print(f" - {name}: {val} {unit}")

    # 上位10件を一覧（名称順）
    print("\nNutrients (top 10 by name):")
    for name, val, unit in sorted(nutrients, key=lambda x: x[0])[:10]:
        print(f" - {name}: {val} {unit}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run fdc_show_nutrients.py <fdcId>")
        sys.exit(1)
    show_food(int(sys.argv[1]))


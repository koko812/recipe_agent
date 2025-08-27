import json, sys
path = "data/FoodData_Central_foundation_food_json_2025-04-24.json"

with open(path, "r", encoding="utf-8") as f:
    raw = json.load(f)  # ← ここは file handle を渡す

# 配列 or dict(FDCは 'FoundationFoods' キーなどを持つことがある)
if isinstance(raw, list):
    items = raw
elif isinstance(raw, dict):
    # Foundation / Legacy でキー名が違う場合があるので順に探す
    for k in ("FoundationFoods", "foods", "BrandedFoods", "SurveyFoods", "SRLegacyFoods"):
        if k in raw:
            items = raw[k]
            break
    else:
        print("食品配列が見つかりません", file=sys.stderr)
        items = []
else:
    print("未知のトップレベル型:", type(raw), file=sys.stderr)
    items = []

print(type(raw), "len(items)=", len(items))
# 参考: 各アイテムは description, foodNutrients などを持つ（例はハマス/トマト）。:contentReference[oaicite:0]{index=0}

# 1) 栄養素の種類をユニーク化＋出現頻度
from collections import Counter

freq = Counter()
meta = {}  # nutrient_id -> (name, number, unit)

for it in items:
    for fn in it.get("foodNutrients", []):
        n = (fn.get("nutrient") or {})
        nid = n.get("id")
        if not nid:
            continue
        meta[nid] = (n.get("name"), n.get("number"), n.get("unitName"))
        freq[nid] += 1

# 上位だけざっと確認
for nid, c in freq.most_common(200):
    name, number, unit = meta[nid]
    print(f"{name} (#{number}, {unit}) — {c} foods")


print(len(meta))

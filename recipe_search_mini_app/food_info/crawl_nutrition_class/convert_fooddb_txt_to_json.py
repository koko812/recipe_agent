# convert_fooddb_txt_to_json.py
import json
import re
from pathlib import Path

INPUT = "nutritions_fooddb_classes.txt"
OUTPUT = "nutritions_fooddb_classes.json"

# 削除ワード
DROP_WORDS = {"水分", "計", "総量", "脂質", "たんぱく質", 
              "アミノ酸組成によるたんぱく質", "アミノ酸組成計", 
              "トリアシルグリセロール当量", 
              "未同定物質", "アンモニア", "剰余アンモニア"}

def parse_file(path):
    data = {}
    current = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # セクションヘッダ
            if line.startswith("===") and line.endswith("==="):
                current = line.strip("= ").replace(" ", "_").lower()
                data[current] = []
            elif line.startswith("- "):
                if current:
                    item = line[2:].strip()
                    if item and item not in DROP_WORDS:
                        data[current].append(item)
    # 重複削除
    for k,v in data.items():
        seen = set()
        uniq = []
        for x in v:
            if x not in seen:
                uniq.append(x)
                seen.add(x)
        data[k] = uniq
    return data

if __name__ == "__main__":
    parsed = parse_file(INPUT)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)
    print(f"Saved {OUTPUT}")
    for k in parsed:
        print(k, ":", len(parsed[k]), "items")


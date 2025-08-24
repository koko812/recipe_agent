# scrape_batch.py
import time, json
from scrape_one import scrape_publicdomainrecipes  # 既存の関数を使う
from collect_urls import collect_children, START

if __name__ == "__main__":
    targets = collect_children(START) #まずは5件だけ
    print("[targets]")
    for i, rec in enumerate(targets, 1):
        print(f"{i:02d}. {rec['url']}")

    with open("recipes.jsonl", "w", encoding="utf-8") as f:
        for i, rec in enumerate(targets, 1):
            url = rec["url"]
            time.sleep(0.5)  # 優しめに
            try:
                data = scrape_publicdomainrecipes(url)
                # 順番にプリント
                print(f"[{i:02d}] {data['title']}  ({url})  total_time={data['total_time_min']}")
                # 保存（1行1レシピ）
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
            except Exception as e:
                print(f"[{i:02d}] NG {url} -> {e}")


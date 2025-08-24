# filter_recipes.py
import json

def is_recipe(rec: dict) -> tuple[bool, str]:
    if not rec.get("title"):
        return False, "no_title"
    ings = rec.get("ingredients_raw") or []
    dirs = rec.get("directions_raw") or []
    if len(ings) >= 2 or len(dirs) >= 2:
        return True, ""
    return False, f"too_sparse(ings={len(ings)},dirs={len(dirs)})"

def run(src="recipes_depth1.jsonl", dst="recipes_filtered.jsonl", skipped="skipped.jsonl"):
    seen_urls = set()
    keep, drop = 0, 0
    with open(src, "r", encoding="utf-8") as fin, \
         open(dst, "w", encoding="utf-8") as fout, \
         open(skipped, "w", encoding="utf-8") as ferr:
        for line in fin:
            rec = json.loads(line)
            url = (rec.get("url") or "").rstrip("/")
            if url in seen_urls:
                ferr.write(json.dumps({"url": url, "reason": "dup_url"}) + "\n"); drop += 1; continue
            seen_urls.add(url)

            ok, why = is_recipe(rec)
            if ok:
                fout.write(json.dumps(rec, ensure_ascii=False) + "\n"); keep += 1
            else:
                ferr.write(json.dumps({"url": url, "reason": why}) + "\n"); drop += 1
    print(f"kept={keep}, skipped={drop}, total={keep+drop}")

if __name__ == "__main__":
    run()


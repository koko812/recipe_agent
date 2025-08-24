# count_chars.py
import json, sys, statistics

SRC = sys.argv[1] if len(sys.argv) > 1 else "recipes_filtered.jsonl"

def rec_len(rec: dict) -> int:
    title = rec.get("title") or ""
    ings  = rec.get("ingredients_raw") or []
    dirs  = rec.get("directions_raw") or []
    # 文字数（改行や区切りは足さず、純粋に各要素の len() を合算）
    return len(title) + sum(len(s) for s in ings) + sum(len(s) for s in dirs)

def main():
    total_chars = 0
    per_rec = []
    n = 0
    with open(SRC, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            n += 1
            L = rec_len(rec)
            per_rec.append(L)
            total_chars += L

    avg = total_chars / n if n else 0
    p50 = statistics.median(per_rec) if per_rec else 0
    p90 = statistics.quantiles(per_rec, n=10)[8] if len(per_rec) >= 10 else avg

    print(f"file        : {SRC}")
    print(f"recipes     : {n}")
    print(f"total_chars : {total_chars:,}")
    print(f"avg_per_rec : {avg:,.1f}")
    print(f"median      : {p50:,.1f}")
    print(f"p90         : {p90:,.1f}")

if __name__ == "__main__":
    main()


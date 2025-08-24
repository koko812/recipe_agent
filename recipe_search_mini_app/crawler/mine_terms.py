# mine_terms.py
import json, re, collections, csv

# ざっくり除外（増やしたくなったらここへ）
STOP = {
    "a","an","the","to","of","and","or","for","in","on","with","into","until","from","at","as","by",
    "it","its","is","are","be","can","should","then","this","that","than","over","under","up","down",
    "you","your","about"
}
# 料理でよく出る単位・ノイズ（必要に応じて追加）
UNITS = {"g","kg","ml","l","cup","cups","tbsp","tsp","teaspoon","teaspoons","tablespoon","tablespoons",
         "ounce","ounces","oz","pound","lb","lbs","°f","°c"}
NUM_RE = re.compile(r"^\d+[\/\-\d]*$")  # 10, 1/2, 350-400 など

def tokenize(s: str):
    # 記号を空白に→小文字化→分割（簡易）
    s = re.sub(r"[^a-zA-Z0-9°\-\/ ]+", " ", s).lower()
    toks = [t for t in s.split() if t]
    return toks

def bigrams(toks):
    return [" ".join(toks[i:i+2]) for i in range(len(toks)-1)]

def keep_token(t):
    if t in STOP or t in UNITS: return False
    if NUM_RE.match(t): return False
    if len(t) <= 2 and t not in {"oil","egg"}: return False
    return True

def mine(jsonl_path: str, topn: int = 50):
    ing_unigram = collections.Counter()
    ing_bigram  = collections.Counter()
    dir_unigram = collections.Counter()
    dir_bigram  = collections.Counter()

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            # 材料
            for row in rec.get("ingredients_raw", []):
                toks = [t for t in tokenize(row) if keep_token(t)]
                ing_unigram.update(toks)
                ing_bigram.update([b for b in bigrams(toks) if all(keep_token(x) for x in b.split())])
            # 手順
            for row in rec.get("directions_raw", []):
                toks = [t for t in tokenize(row) if keep_token(t)]
                dir_unigram.update(toks)
                dir_bigram.update([b for b in bigrams(toks) if all(keep_token(x) for x in b.split())])

    # 画面にさっと出す
    print("\n[INGREDIENT TERMS — UNIGRAM]")
    for w,c in ing_unigram.most_common(topn): print(f"{w}\t{c}")
    print("\n[INGREDIENT TERMS — BIGRAM]")
    for w,c in ing_bigram.most_common(topn): print(f"{w}\t{c}")

    print("\n[TECHNIQUE TERMS — UNIGRAM]")
    for w,c in dir_unigram.most_common(topn): print(f"{w}\t{c}")
    print("\n[TECHNIQUE TERMS — BIGRAM]")
    for w,c in dir_bigram.most_common(topn): print(f"{w}\t{c}")

    # CSVにも保存（後で見返せる）
    def dump(fname, counter):
        with open(fname, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["term","count"])
            for term, cnt in counter.most_common():
                w.writerow([term, cnt])
    dump("terms_ingredients_unigram.csv", ing_unigram)
    dump("terms_ingredients_bigram.csv",  ing_bigram)
    dump("terms_directions_unigram.csv",  dir_unigram)
    dump("terms_directions_bigram.csv",   dir_bigram)

if __name__ == "__main__":
    mine("recipes_depth1.jsonl", topn=40)   # ←ファイル名は手元のJSONLに合わせて


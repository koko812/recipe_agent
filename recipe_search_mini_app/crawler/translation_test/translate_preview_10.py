# translate_preview_10.py
import os, json, itertools

# DeepL を使うかどうか切り替え
USE_DEEPL = True   # False にすると「ダミー: 英文そのまま」になります

def translate_batch(texts):
    """テキストのリストをまとめて翻訳して返す"""
    if not texts:
        return []
    if USE_DEEPL:
        import deepl
        auth = os.environ["DEEPL_API_KEY"]  # ← 環境変数にキーを入れておく
        translator = deepl.Translator(auth)
        res = translator.translate_text(texts, target_lang="JA")
        return [r.text for r in res]
    # ダミー：英語をそのまま返す
    return texts

SRC = "recipes_filtered.jsonl"
DST = "recipes_translated_preview.jsonl"
N   = 10   # 10件だけ翻訳

def main():
    out = open(DST, "w", encoding="utf-8")
    count = 0
    with open(SRC, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            title_en = rec.get("title") or ""
            ings_en  = rec.get("ingredients_raw") or []
            dirs_en  = rec.get("directions_raw") or []

            # 翻訳リスト作成（title + 材料 + 手順）
            pack = [title_en] + ings_en + dirs_en
            ja = translate_batch(pack)
            if not ja:
                continue

            # 分割
            title_ja = ja[0]
            ings_ja  = ja[1:1+len(ings_en)]
            dirs_ja  = ja[1+len(ings_en):]

            # 画面プレビュー（各カテゴリの最初3件だけ表示）
            print("="*60)
            print("TITLE")
            print("EN:", title_en)
            print("JA:", title_ja)
            print("\nINGREDIENTS")
            for en, j in itertools.islice(zip(ings_en, ings_ja), 3):
                print(" -", en, " => ", j)
            print("\nDIRECTIONS")
            for en, j in itertools.islice(zip(dirs_en, dirs_ja), 3):
                print(" -", en, " => ", j)

            # 保存（日本語版を付加してJSONL）
            rec_out = dict(rec)
            rec_out["title_ja"]       = title_ja
            rec_out["ingredients_ja"] = ings_ja
            rec_out["directions_ja"]  = dirs_ja
            out.write(json.dumps(rec_out, ensure_ascii=False) + "\n")

            count += 1
            if count >= N:
                break

    out.close()
    print(f"\nSaved preview -> {DST} (count={count})")

if __name__ == "__main__":
    main()


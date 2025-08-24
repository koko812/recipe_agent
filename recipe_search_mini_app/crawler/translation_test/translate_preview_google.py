import json, itertools
from google.cloud import translate_v2 as translate

SRC = "recipes_filtered.jsonl"
DST = "recipes_translated_google.jsonl"
N   = 10   # 10件だけ翻訳

# クライアント生成（GOOGLE_APPLICATION_CREDENTIALS 環境変数をセットしておくこと）
translate_client = translate.Client()

def translate_batch(texts, target="ja"):
    """Google Translate APIでまとめて翻訳"""
    if not texts: 
        return []
    result = translate_client.translate(texts, target_language=target)
    return [r["translatedText"] for r in result]

def main():
    out = open(DST, "w", encoding="utf-8")
    count = 0
    with open(SRC, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            title_en = rec.get("title") or ""
            ings_en  = rec.get("ingredients_raw") or []
            dirs_en  = rec.get("directions_raw") or []

            pack = [title_en] + ings_en + dirs_en
            ja = translate_batch(pack)

            title_ja = ja[0]
            ings_ja  = ja[1:1+len(ings_en)]
            dirs_ja  = ja[1+len(ings_en):]

            # 画面プレビュー
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

            # 保存
            rec_out = dict(rec)
            rec_out["title_ja"] = title_ja
            rec_out["ingredients_ja"] = ings_ja
            rec_out["directions_ja"] = dirs_ja
            out.write(json.dumps(rec_out, ensure_ascii=False) + "\n")

            count += 1
            if count >= N:
                break

    out.close()
    print(f"\nSaved preview -> {DST} (count={count})")

if __name__ == "__main__":
    main()


# app.py（差し替え部分だけ）
from fastapi import FastAPI
from typing import List
from models import Recipe, SearchRequest, Ingredient
from db import get_connection  # ← 追加

app = FastAPI()

@app.post("/search", response_model=List[Recipe])
def search(req: SearchRequest) -> List[Recipe]:
    toks = [t for t in req.query.replace("　", " ").split() if t]
    if not toks:
        return []

    conn = get_connection()
    cur = conn.cursor()

    # 各キーワード t について：
    #   (タイトルに LIKE '%t%' もしくは 材料名に LIKE '%t%') を OR でまとめる
    base_sql = """
        SELECT r.id, r.title, r.url, r.total_time_min,
               i.name AS ing_name, i.quantity AS ing_qty, i.unit AS ing_unit
        FROM recipes r
        LEFT JOIN recipe_ingredients i ON i.recipe_id = r.id
        WHERE 1=1
    """
    params: list[str] = []
    conds: list[str] = []  # ← 追加

    for _t in toks:
        conds.append(
            """
            (r.title LIKE ? OR EXISTS (
                SELECT 1 FROM recipe_ingredients i2
                WHERE i2.recipe_id = r.id AND i2.name LIKE ?
            ))
            """
        )
        like = f"%{_t}%"
        params.extend([like, like])

    # ループ外で完成形を作る（toks が空なら素通し）
    sql = base_sql + ("" if not conds else " AND (" + " OR ".join(conds) + ")")
    print("SQL:", sql)
    print("params:", params)

    rows = cur.execute(sql, params).fetchall()

    # ← これを追加：0件ならここで返す（IndexError回避）
    if not rows:
        conn.close()
        return []

    #print(rows[0].keys())   # 取り出せるカラム名
    #print(dict(rows[0]))    # 1行を辞書化して中身を見る
    print(f"[DEBUG] rows={len(rows)}件")
    for i, row in enumerate(rows[:10]):  # 先頭10行だけ
        print(f"[{i}] id={row['id']} title={row['title']} ing={row['ing_name']} qty={row['ing_qty']} unit={row['ing_unit']}")
    conn.close()

    # レシピ単位にまとめ直す
    by_id: dict[int, Recipe] = {}
    for row in rows:
        rid = row["id"]
        if rid not in by_id:
            by_id[rid] = Recipe(
                id=rid,
                title=row["title"],
                url=row["url"],
                total_time_min=row["total_time_min"],
                ingredients=[],
            )
        # LEFT JOIN のため NULL の材料行があり得る
        if row["ing_name"] is not None:
            by_id[rid].ingredients.append(
                Ingredient(name=row["ing_name"], quantity=row["ing_qty"], unit=row["ing_unit"])
            )

    # マッチ件数0や、同一レシピで複数行→まとめ済み
    return list(by_id.values())


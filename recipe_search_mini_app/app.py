from fastapi import FastAPI
from typing import List
from models import Recipe, SearchRequest, Ingredient

app = FastAPI()

# とりあえずインメモリのダミーデータ
RECIPES: List[Recipe] = [
    Recipe(
        id=1,
        title="とりのねぎ塩炒め",
        url="https://example.com/negishio",
        total_time_min=10,
        ingredients=[Ingredient(name="鶏むね肉", quantity=200, unit="g"),
                     Ingredient(name="長ねぎ", quantity=1, unit="本")]
    ),
    Recipe(
        id=2,
        title="長ねぎたっぷり親子丼（軽め）",
        url="https://example.com/oyakodon",
        total_time_min=15,
        ingredients=[Ingredient(name="鶏もも肉", quantity=150, unit="g"),
                     Ingredient(name="卵", quantity=2, unit="個"),
                     Ingredient(name="長ねぎ", quantity=1, unit="本")]
    ),
]

@app.post("/search", response_model=List[Recipe])
def search(req: SearchRequest) -> List[Recipe]:
    # 超簡単：ANDマッチ（全てのキーワードがタイトルor食材名に含まれる）
    toks = [t for t in req.query.replace("　", " ").split() if t]
    def match(r: Recipe) -> bool:
        hay = " ".join([r.title] + [i.name for i in r.ingredients])
        return all(t in hay for t in toks)
    return [r for r in RECIPES if match(r)]


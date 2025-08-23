# tools/recipe_search.py
from typing import List
from schemas import RecipeQuery, RecipeCandidate

def find_recipes_mock(q: RecipeQuery) -> List[RecipeCandidate]:
    # 後で本物のWeb検索に置換する。今はスコアだけ“それっぽく”
    title = f"{'とり' if '鶏' in ''.join(q.ingredients) else 'かんたん'}のねぎ塩炒め"
    return [
        RecipeCandidate(
            title=title,
            url="https://example.com/recipe/negishio",
            ingredients=["鶏むね肉", "長ねぎ", "塩", "ごま油"],
            summary="10分で作れる高タンパク。長ねぎで香りと旨味を補強、油は控えめ。",
            score=0.82 + (0.05 if "時短" in q.constraints else 0) + (0.03 if "低脂質" in q.constraints else 0),
        ),
        RecipeCandidate(
            title="長ねぎたっぷり親子丼（軽め）",
            url="https://example.com/recipe/oyakodon",
            ingredients=["鶏もも肉", "卵", "長ねぎ", "だし"],
            summary="卵でボリューム、だし薄めでも満足感。脂を落として軽めに。",
            score=0.74,
        ),
    ]


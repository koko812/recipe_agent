# prefer_jsonld.py
import requests, json, extruct
from w3lib.html import get_base_url

def extract_recipe_jsonld(url: str):
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=20)
    data = extruct.extract(r.text, base_url=get_base_url(r.text, r.url), syntaxes=["json-ld"])
    recipes = []
    for item in data.get("json-ld", []):
        t = item.get("@type")
        if t == "Recipe" or (isinstance(t, list) and "Recipe" in t):
            recipes.append(item)
    return recipes

if __name__ == "__main__":
    for rec in extract_recipe_jsonld("https://publicdomainrecipes.com/basic-waffles/"):
        print(json.dumps({k: rec.get(k) for k in ["name","recipeIngredient","recipeInstructions"]}, ensure_ascii=False, indent=2))


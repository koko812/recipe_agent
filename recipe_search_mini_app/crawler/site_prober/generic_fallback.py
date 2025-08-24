# generic_fallback.py
from bs4 import BeautifulSoup
import requests

def next_list_after(h, max_steps=5):
    sib = h
    for _ in range(max_steps):
        sib = sib.find_next_sibling()
        if not sib: break
        if sib.name in ("ul","ol"): return sib
    return None

def fallback(url: str):
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    def section(name):
        for h in soup.select("h1,h2,h3"):
            t = h.get_text(" ", strip=True).lower()
            if "ingredient" in t and name=="ingredients":
                return [li.get_text(" ", strip=True) for li in (next_list_after(h) or []).select("li")]
            if "direction" in t or "instruction" in t:
                if name=="directions":
                    return [li.get_text(" ", strip=True) for li in (next_list_after(h) or []).select("li")]
        return []

    return {
        "title": (soup.select_one("h1") or soup.select_one("title")).get_text(strip=True),
        "ingredients": section("ingredients"),
        "directions": section("directions"),
    }


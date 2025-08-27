# chebi_lite_demo.py
# 使い方:
#   1) chebi_lite.json.gz をローカルに置く
#   2) uv run chebi_lite_demo.py

import json, gzip
from collections import defaultdict, deque

CHEBI_LITE_PATH = "data/chebi_lite.json.gz"  # 公式の lite JSON（約10MB）

def load_chebi_lite(path=CHEBI_LITE_PATH):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        data = json.load(f)
    # data["graphs"][0]["nodes"] / ["edges"] という OBO Graph 風JSONが一般的
    g = data["graphs"][0]
    nodes = g["nodes"]
    edges = g.get("edges", [])
    return nodes, edges

def build_indexes(nodes, edges):
    id2name = {}
    name2ids = defaultdict(set)
    children = defaultdict(set)

    for n in nodes:
        cid = n["id"]  # 例: "CHEBI:35366"
        lbl = n.get("lbl", "")
        if lbl:
            id2name[cid] = lbl
            name2ids[lbl.lower()].add(cid)
        # 同義語（英語中心）
        for syn in n.get("meta", {}).get("synonyms", []):
            s = syn.get("val", "")
            if s:
                name2ids[s.lower()].add(cid)

    for e in edges:
        if e.get("pred") in ("is_a", "rdfs:subClassOf"):
            parent = e["sub"]
            super_ = e["obj"]
            children[super_].add(parent)

    return id2name, name2ids, children

def descendants(root_id, children):
    """BFS で root のすべての子孫 ID を列挙"""
    out, q = set(), deque([root_id])
    while q:
        cur = q.popleft()
        for ch in children.get(cur, []):
            if ch not in out:
                out.add(ch)
                q.append(ch)
    return out

if __name__ == "__main__":
    nodes, edges = load_chebi_lite()
    id2name, name2ids, children = build_indexes(nodes, edges)

    # 例1) “fatty acid” の子孫を列挙
    fatty_acid_id = next(iter(name2ids["fatty acid"]))  # 代表IDを1つ
    fa_desc = descendants(fatty_acid_id, children)
    print("fatty acid descendants (sample 15):")
    for i, cid in enumerate(sorted(fa_desc)[:15], 1):
        print(f"{i:02d}. {cid}  {id2name.get(cid,'')}")
    print(f"... total {len(fa_desc)} nodes")

    # 例2) 名前から ID を引く（同義語も対応）
    for q in ["palmitic acid", "oleic acid", "citric acid", "lactic acid"]:
        print(q, "->", sorted(name2ids.get(q.lower(), [])))


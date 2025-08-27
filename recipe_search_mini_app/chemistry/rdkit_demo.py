from rdkit import Chem
from rdkit.Chem import Draw

smiles_list = [
    "C1=CC=C(C=C1)C=O",             # Benzaldehyde
    "COC1=CC=C(C=O)C=C1O",          # Vanillin（より一般的な表記）
    "C1=CC=C2N=CN=C2N1",            # Benzimidazole（色素そのものではないが親骨格）
    "CC(=C)C=C(C)C=C(C)C=C(C)C=C(C)C=C(C)C"  # 簡略カロテノイド鎖（学習用ダミー）
]
mols = [Chem.MolFromSmiles(s) for s in smiles_list]
img = Draw.MolsToImage(mols, legends=["Benzaldehyde","Vanillin","Benzimidazole","Polyene-like"])
img.save("molecules.png")
print("saved: molecules.png")


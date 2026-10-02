import pandas as pd

web = pd.read_excel("data/Fichier_web.xlsx")

web_clean = web[
    web["post_type"] == "product"
]

print("Lignes après filtrage :", len(web_clean))
print("SKU uniques :", web_clean["sku"].nunique())
print("Doublons SKU :", len(web_clean) - web_clean["sku"].nunique())
import pandas as pd

web = pd.read_excel("data/Fichier_web.xlsx")

web_clean = web[
    web["post_type"] == "product"
]

duplicates = web_clean[
    web_clean["sku"].duplicated(keep=False)
]

print(
    duplicates[
        ["sku", "post_title", "post_name"]
    ].sort_values("sku")
)
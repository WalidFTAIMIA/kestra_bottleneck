import pandas as pd

web = pd.read_excel("data/Fichier_web.xlsx")

print("Nombre de lignes :", len(web))

print("\nValeurs manquantes :")
print(web.isnull().sum())

print("\nSKU uniques :", web["sku"].nunique())

print("Doublons SKU :", len(web) - web["sku"].nunique())
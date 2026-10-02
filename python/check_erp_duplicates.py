import pandas as pd

erp = pd.read_excel("data/Fichier_erp.xlsx")

total = len(erp)

unique = erp["product_id"].nunique()

print("Nombre total de lignes :", total)
print("Nombre de product_id uniques :", unique)
print("Doublons :", total - unique)
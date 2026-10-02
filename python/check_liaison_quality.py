import pandas as pd

liaison = pd.read_excel("data/fichier_liaison.xlsx")

print("Nombre de lignes :", len(liaison))

print("\nValeurs manquantes :")
print(liaison.isnull().sum())

print("\nProduct_id uniques :", liaison["product_id"].nunique())

print("Doublons product_id :",
      len(liaison) - liaison["product_id"].nunique())

print("\nId_web uniques :", liaison["id_web"].nunique())

print("Doublons id_web :",
      len(liaison) - liaison["id_web"].nunique())

missing_id_web = liaison["id_web"].isna().sum()
assert liaison["product_id"].notna().all(), "product_id liaison manquant"
assert liaison["product_id"].is_unique, "product_id liaison non unique"
print("Correspondances WEB absentes (id_web manquant) :", missing_id_web)
import pandas as pd

erp = pd.read_excel("data/Fichier_erp.xlsx")

print(erp.head())

print("\nNombre de lignes :", len(erp))

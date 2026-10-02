import pandas as pd

erp = pd.read_excel("data/Fichier_erp.xlsx")
web = pd.read_excel("data/Fichier_web.xlsx")
liaison = pd.read_excel("data/fichier_liaison.xlsx")

print("=== ERP ===")
print(erp.columns.tolist())

print("\n=== WEB ===")
print(web.columns.tolist())

print("\n=== LIAISON ===")
print(liaison.columns.tolist())
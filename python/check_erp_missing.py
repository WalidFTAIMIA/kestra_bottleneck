import pandas as pd

erp = pd.read_excel("data/Fichier_erp.xlsx")

print(erp.isnull().sum())
import pandas as pd

liaison = pd.read_excel("data/fichier_liaison.xlsx")

liaison_not_null = liaison.dropna(subset=["id_web"])

duplicates = liaison_not_null["id_web"].duplicated().sum()
print("Doublons réels id_web :", duplicates)
assert duplicates == 0, "Doublons id_web detectes"
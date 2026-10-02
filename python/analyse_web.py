import pandas as pd

web = pd.read_excel("data/Fichier_web.xlsx")

print(web["post_type"].value_counts())
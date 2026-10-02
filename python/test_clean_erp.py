import pandas as pd
import duckdb

# Lecture du fichier ERP
erp = pd.read_excel("data/Fichier_erp.xlsx")

# Connexion DuckDB
conn = duckdb.connect()

# Enregistrement de la dataframe sous le nom "erp"
conn.register("erp", erp)

# Lecture du script SQL
with open("sql/clean_erp.sql", "r") as f:
    sql = f.read()

# Exécution
conn.execute(sql)

# Vérification
result = conn.execute("""
SELECT COUNT(*)
FROM erp_clean
""").fetchone()

print("Nombre de lignes ERP nettoyées :", result[0])

conn.close()

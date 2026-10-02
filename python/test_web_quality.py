import pandas as pd
import duckdb

# Lecture du fichier WEB
web = pd.read_excel("data/Fichier_web.xlsx")

# Connexion DuckDB
conn = duckdb.connect()

# Enregistrement de la dataframe
conn.register("web", web)

# Exécution du nettoyage
with open("sql/clean_web.sql") as f:
    conn.execute(f.read())

# Exécution du test
with open("sql/test_web.sql") as f:
    result = conn.execute(f.read()).fetchone()

print("Nombre de doublons WEB :", result[0])
assert result[0] == 0, "Doublons WEB detectes"

# Comptage des lignes après nettoyage
rows = conn.execute("""
SELECT COUNT(*)
FROM web_clean
""").fetchone()

print("Nombre de lignes WEB nettoyées :", rows[0])
assert rows[0] > 0, "Aucune ligne WEB nettoyee"

clean_web = conn.execute("SELECT sku FROM web_clean").fetchdf()
assert clean_web["sku"].notna().all(), "SKU WEB manquant"
assert clean_web["sku"].is_unique, "SKU WEB non unique apres nettoyage"

conn.close()
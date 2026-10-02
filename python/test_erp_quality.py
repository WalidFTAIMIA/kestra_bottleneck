import pandas as pd
import duckdb

erp = pd.read_excel("data/Fichier_erp.xlsx")

conn = duckdb.connect()

conn.register("erp", erp)

# Nettoyage
with open("sql/clean_erp.sql") as f:
    conn.execute(f.read())

# Test
with open("sql/test_erp.sql") as f:
    result = conn.execute(f.read()).fetchone()

print("Nombre de doublons ERP :", result[0])
assert result[0] == 0, "Doublons ERP detectes"
assert erp["product_id"].notna().all(), "product_id ERP manquant"
assert erp["product_id"].is_unique, "product_id ERP non unique"

conn.close()
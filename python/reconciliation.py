import duckdb

# Les sources et les tables nettoyees sont preparees par les etapes precedentes.
conn = duckdb.connect("bottleneck.db")

with open("sql/reconciliation.sql") as file:
    conn.execute(file.read())

# Aperçu
resultat = conn.execute("""
SELECT *
FROM ventes
LIMIT 10
""").fetchdf()

print("\n=== APERCU VENTES ===")
print(resultat)

conn.close()
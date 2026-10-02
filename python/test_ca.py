import duckdb

conn = duckdb.connect("bottleneck.db")

stats = conn.execute("""
SELECT
    COUNT(*) AS nb_produits,
    SUM(chiffre_affaires) AS ca_total
FROM ca_produit
""").fetchone()

nb_produits, ca_total = stats

print("Nombre produits :", nb_produits)
print("CA total :", round(ca_total, 2))

assert nb_produits > 0, "Aucun produit dans ca_produit"
assert ca_total >= 0, "CA total negatif"

conn.close()
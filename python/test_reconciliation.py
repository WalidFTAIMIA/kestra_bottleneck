import duckdb

conn = duckdb.connect("bottleneck.db")

stats = conn.execute("""
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT product_id) AS unique_products
FROM ventes
""").fetchone()

total_rows = stats[0]
unique_products = stats[1]

print("\n=== TEST RECONCILIATION ===")
print("Total lignes :", total_rows)
print("Produits uniques :", unique_products)

# Contrôles métier
assert total_rows > 500, "Volume de données anormalement faible"
assert total_rows == unique_products, "Doublons détectés après réconciliation"

null_product = conn.execute("""
SELECT COUNT(*)
FROM ventes
WHERE product_id IS NULL
""").fetchone()[0]

assert null_product == 0, "Product_id NULL détecté"

print("\n Réconciliation validée")

conn.close()
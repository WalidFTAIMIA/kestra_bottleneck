import pandas as pd
import duckdb

# Connexion à DuckDB
conn = duckdb.connect("bottleneck.db")

# Lecture des données
df = conn.execute("""
SELECT *
FROM ca_produit
""").fetchdf()

# Calcul de la moyenne des prix
moyenne = df["price"].mean()

# Calcul de l'écart-type
ecart_type = df["price"].std()

# Calcul du Z-Score
df["z_score"] = (
    df["price"] - moyenne
) / ecart_type

# Classification
df["categorie"] = df["z_score"].apply(
    lambda x: "premium"
    if x > 2
    else "ordinaire"
)

# Comptages
premium = df[df["categorie"] == "premium"]
ordinaire = df[df["categorie"] == "ordinaire"]

print("\n=== Résultats Z-Score ===")
print("Prix moyen :", round(moyenne, 2))
print("Écart-type :", round(ecart_type, 2))
print("Nombre de vins premium :", len(premium))
print("Nombre de vins ordinaires :", len(ordinaire))

assert len(df) > 0, "Aucune donnee pour le Z-score"
assert df["z_score"].notna().all(), "Z-score manquant detecte"
assert len(premium) + len(ordinaire) == len(df), "Classification Z-score incomplete"

print("\n=== Top 10 vins premium ===")
print(
    premium[
        ["product_id", "price", "z_score"]
    ]
    .sort_values("z_score", ascending=False)
    .head(10)
)

conn.close()
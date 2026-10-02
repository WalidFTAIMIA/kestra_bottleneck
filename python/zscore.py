import pandas as pd
import duckdb

# Connexion à DuckDB
conn = duckdb.connect("bottleneck.db")

# Lecture de la table ca_produit
df = conn.execute("""
SELECT *
FROM ca_produit
""").fetchdf()

# Calcul de la moyenne
moyenne = df["price"].mean()

# Calcul de l'écart-type
ecart_type = df["price"].std()

# Calcul du Z-Score
df["z_score"] = (
    df["price"] - moyenne
) / ecart_type

# Classification
df["categorie"] = df["z_score"].apply(
    lambda x: "premium" if x > 2 else "ordinaire"
)

# Exports
premium = df[df["categorie"] == "premium"]
ordinaire = df[df["categorie"] == "ordinaire"]

premium.to_csv(
    "premium.csv",
    index=False
)

ordinaire.to_csv(
    "ordinaire.csv",
    index=False
)

print("Nombre de vins premium :", len(premium))
print("Nombre de vins ordinaires :", len(ordinaire))

conn.close()
import pandas as pd
import duckdb

# Connexion à la base DuckDB
conn = duckdb.connect("bottleneck.db")

# Creation de la table de calcul avant la generation du rapport.
with open("sql/ca.sql") as file:
    conn.execute(file.read())

# Récupération de la table ventes
ventes = conn.execute("""
SELECT *
FROM ventes
""").df()

# Calcul du chiffre d'affaires par produit
ventes["chiffre_affaires"] = (
    ventes["price"] *
    ventes["total_sales"]
)

# Calcul du chiffre d'affaires total
ca_total = ventes["chiffre_affaires"].sum()

print("\n=== Chiffre d'affaires total ===")
print(round(ca_total, 2), "€")

# Export du détail CA par produit
with pd.ExcelWriter("rapport_ca.xlsx") as writer:

    ventes.to_excel(
        writer,
        sheet_name="CA_Produit",
        index=False
    )

    pd.DataFrame(
        {"CA_Total": [ca_total]}
    ).to_excel(
        writer,
        sheet_name="CA_Total",
        index=False
    )

print("\nFichier rapport_ca.xlsx généré avec succès")
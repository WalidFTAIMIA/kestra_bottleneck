CREATE OR REPLACE TABLE ca_produit AS
SELECT
    product_id,
    price,
    total_sales,
    price * total_sales AS chiffre_affaires
FROM ventes;
CREATE OR REPLACE TABLE ventes AS

SELECT
    e.product_id,
    e.price,
    e.stock_quantity,
    w.total_sales,
    w.post_title

FROM erp_clean e

INNER JOIN liaison_clean l
    ON e.product_id = l.product_id

INNER JOIN web_clean w
    ON CAST(l.id_web AS VARCHAR)
       = CAST(w.sku AS VARCHAR)

WHERE w.total_sales IS NOT NULL;
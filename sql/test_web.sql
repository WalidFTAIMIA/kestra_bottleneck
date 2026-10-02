SELECT
COUNT(*) - COUNT(DISTINCT sku)
AS duplicate_sku
FROM web_clean;
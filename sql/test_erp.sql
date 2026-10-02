SELECT
COUNT(*) - COUNT(DISTINCT product_id)
AS duplicate_product_id
FROM erp_clean  ;
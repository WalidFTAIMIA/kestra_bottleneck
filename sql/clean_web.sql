CREATE OR REPLACE TABLE web_clean AS
SELECT DISTINCT *
FROM web
WHERE post_type = 'product'
  AND sku IS NOT NULL;
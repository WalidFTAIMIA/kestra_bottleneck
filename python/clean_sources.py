import duckdb

conn = duckdb.connect("bottleneck.db")

with open("sql/clean_erp.sql") as file:
    conn.execute(file.read())

with open("sql/clean_web.sql") as file:
    conn.execute(file.read())

with open("sql/clean_liaison.sql") as file:
    conn.execute(file.read())

for table_name in ("erp_clean", "web_clean", "liaison_clean"):
    count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"Table {table_name} : {count} lignes")

conn.close()

import duckdb
import pandas as pd

conn = duckdb.connect("bottleneck.db")

sources = {
    "erp": "data/Fichier_erp.xlsx",
    "web": "data/Fichier_web.xlsx",
    "liaison": "data/fichier_liaison.xlsx",
}

for table_name, file_path in sources.items():
    dataframe = pd.read_excel(file_path)
    conn.register(f"{table_name}_df", dataframe)
    conn.execute(
        f"CREATE OR REPLACE TABLE {table_name} AS "
        f"SELECT * FROM {table_name}_df"
    )
    conn.unregister(f"{table_name}_df")
    print(f"Source {table_name} importee : {len(dataframe)} lignes")

conn.close()

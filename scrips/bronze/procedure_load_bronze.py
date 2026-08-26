"""
load_bronze.py
Carga los CSV de origen a las tablas de la capa bronze en PostgreSQL (Neon).

Equivalente en Python al procedure 'bronze.load_bronze' de SQL Server
(TRUNCATE + BULK INSERT + logging de tiempos + manejo de errores).

Requiere:
    pip install psycopg2-binary python-dotenv

Uso:
    python load_bronze.py
"""

import os
import time
import psycopg2
from dotenv import load_dotenv

# Carga las variables PGHOST, PGDATABASE, PGUSER, PGPASSWORD, etc. desde .env
load_dotenv()

# Tablas a cargar: (nombre_tabla, ruta_csv)
TABLES = [
    ("bronze.crm_cust_info", "datasets/source_crm/cust_info.csv"),
    ("bronze.crm_prd_info", "datasets/source_crm/prd_info.csv"),
    ("bronze.crm_sales_details", "datasets/source_crm/sales_details.csv"),
    ("bronze.erp_loc_a101", "datasets/source_erp/loc_a101.csv"),
    ("bronze.erp_cust_az12", "datasets/source_erp/cust_az12.csv"),
    ("bronze.erp_px_cat_g1v2", "datasets/source_erp/px_cat_g1v2.csv"),
]


def load_bronze():
    conn = None
    batch_start = time.time()
    try:
        conn = psycopg2.connect(
            host=os.environ["PGHOST"],
            dbname=os.environ["PGDATABASE"],
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"],
            sslmode=os.environ.get("PGSSLMODE", "require"),
        )
        conn.autocommit = False
        cur = conn.cursor()

        print("=" * 50)
        print("Loading Bronze Layer")
        print("=" * 50)

        current_group = None
        for table, path in TABLES:
            group = "CRM Tables" if "crm_" in table else "ERP Tables"
            if group != current_group:
                current_group = group
                print("-" * 50)
                print(f"Loading {group}")
                print("-" * 50)

            start = time.time()
            print(f">> Truncating Table: {table}")
            cur.execute(f"TRUNCATE TABLE {table};")

            print(f">> Inserting Data Into: {table}")
            with open(path, "r", encoding="utf-8") as f:
                cur.copy_expert(
                    f"COPY {table} FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ',')",
                    f,
                )

            conn.commit()
            elapsed = round(time.time() - start, 2)
            print(f">> Load Duration: {elapsed} seconds")
            print(">> -------------")

        batch_elapsed = round(time.time() - batch_start, 2)
        print("=" * 50)
        print("Loading Bronze Layer is Completed")
        print(f"   - Total Load Duration: {batch_elapsed} seconds")
        print("=" * 50)

    except Exception as e:
        if conn:
            conn.rollback()
        print("=" * 50)
        print("ERROR OCCURRED DURING LOADING BRONZE LAYER")
        print(f"Error Message: {e}")
        print("=" * 50)

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    load_bronze()

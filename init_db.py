"""
init_db.py  -  Build (or rebuild) the pharmacy database.

Runs schema.sql (DDL) and then seed.sql (DML) to create a fresh
pharmacy.db file with all tables and at least 20 records per table.

Usage:
    python init_db.py
"""

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pharmacy.db")
SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")
SEED_FILE = os.path.join(BASE_DIR, "seed.sql")

TABLES = ["Category", "Supplier", "Medicine", "Customer",
          "Employee", "Sale", "Sale_Item"]


def run_sql_file(conn, path):
    with open(path, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def build():
    # Start from a clean slate every time.
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
        run_sql_file(conn, SCHEMA_FILE)   # DDL : create tables
        run_sql_file(conn, SEED_FILE)     # DML : insert records
        conn.commit()

        print("Database created at:", DB_PATH)
        print("-" * 40)
        for table in TABLES:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table:<12} : {count:>3} records")
        print("-" * 40)
        print("Done. Run 'python app.py' to open the application.")
    finally:
        conn.close()


if __name__ == "__main__":
    build()

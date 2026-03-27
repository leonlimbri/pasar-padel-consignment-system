"""utils/connection.py
Handles all SQLite database connections and query execution.
Also defines shared dropdown option constants used across pages.
"""

import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# ── Database & SQL path config ────────────────────────────────────────────────
DB_PATH  = os.getenv("DB_PATH")
SQL_PATH = os.getenv("SQL_PATH")

# ── Shared dropdown options ───────────────────────────────────────────────────
consignment_type_options = ["Racket", "Shirt", "Shoes", "Bag", "Others"]
status_type_options      = ["New", "Posted", "Sold", "Shipped", "Completed", "Completed Elsewhere"]


def run_query(query: str):
    """Execute a raw SQL string against the database.

    - For INSERT / UPDATE / DELETE: commits and returns None.
    - For SELECT: returns a list of dicts (one per row).
    - Returns None on any exception (errors are silently swallowed).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        is_write = query.upper().startswith(("INSERT", "UPDATE", "DELETE"))
        if is_write:
            cursor.execute(query)
            conn.commit()
            conn.close()
        else:
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]

    except Exception as e:
        print(f"[DB ERROR] {e}")
        return None

def run_query_from_sql(fn: str, fp: str = SQL_PATH, print_sql: bool = False, **kwargs):
    """Load a .sql file, interpolate kwargs, and run it.

    Args:
        fn:        Filename of the SQL script (e.g. "get_all_consignments.sql").
        fp:        Folder path where SQL scripts live (defaults to SQL_PATH env var).
        print_sql: If True, prints the final SQL string before executing (debug helper).
        **kwargs:  Named placeholders used by str.format() inside the SQL file.
    """
    filepath = f"{fp}/{fn}"
    with open(filepath) as f:
        query = f.read().format(**kwargs)

    if print_sql:
        print(query)

    return run_query(query)

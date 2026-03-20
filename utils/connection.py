import os, sqlite3
from dotenv import load_dotenv
load_dotenv()

# Connect to the database
DB_PATH = os.getenv("DB_PATH")
SQL_PATH = os.getenv("SQL_PATH")
consignment_type_options = ["Racket", "Shirt", "Shoes", "Bag", "Others"]
status_type_options = ["New", "Posted", "Sold", "Shipped", "Completed", "Completed Elsewhere"]

def run_query(query: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if query.upper().startswith("INSERT") or query.upper().startswith("UPDATE"):
        cursor.execute(query)
        conn.commit()
        conn.close()
    else:
        cursor.execute(query)
        rows = cursor.fetchall()
        dat = [dict(row) for row in rows]
        conn.close()
        return dat
    return None

def run_query_from_sql(fn: str, fp: str = SQL_PATH, print_sql: bool=False,**kwargs):
    _fp = f"{fp}/{fn}"
    with open(_fp) as f:
        q = f.read().format(**kwargs)
        if print_sql: print(q)
        return run_query(q)
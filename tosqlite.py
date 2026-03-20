import sqlite3, os
import pandas as pd

db_path = os.getenv("DB_PATH")
data_folder_path = os.getenv("FOLDER_PATH")
conn = sqlite3.connect(db_path)

for file in os.listdir(data_folder_path):
    print(f"{data_folder_path}/{file}")
    try:
        df = pd.read_csv(f"{data_folder_path}/{file}", encoding="utf-8")
    except:
        df = pd.read_csv(f"{data_folder_path}/{file}", encoding="cp1252")
    tbname = file.replace(".csv", "")
    df.to_sql(
        name=tbname.upper(),
        con=conn,
        if_exists="replace",
        index=False
    )

conn.close()
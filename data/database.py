import sqlite3
import pandas as pd

df = pd.read_csv("data/operaciones_aeropuertos_clean.csv")

conn = sqlite3.connect("data/aeropuertos.db")

df.to_sql(
    "operaciones",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Base de datos creada correctamente")
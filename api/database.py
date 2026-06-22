import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "aeropuertos.db"
CSV_PATH = BASE_DIR / "data" / "operaciones_aeropuertos_clean.csv"


def get_connection():
    crear_base_si_no_existe()
    return sqlite3.connect(DB_PATH)


def crear_base_si_no_existe():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    existe_tabla = pd.read_sql_query(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='operaciones'",
        conn
    )

    if existe_tabla.empty:
        df = pd.read_csv(CSV_PATH)
        df.to_sql("operaciones", conn, if_exists="replace", index=False)

    conn.close()


def obtener_datos(limit=3000):
    conn = get_connection()

    df = pd.read_sql_query(
        f"SELECT * FROM operaciones LIMIT {limit}",
        conn
    )

    conn.close()
    return df


def obtener_estadisticas():
    conn = get_connection()

    query = """
    SELECT 
        COUNT(*) AS total_registros,
        AVG(cnt_operaciones) AS promedio_operaciones,
        MAX(cnt_operaciones) AS maximo_operaciones,
        MIN(cnt_operaciones) AS minimo_operaciones
    FROM operaciones
    """

    stats = pd.read_sql_query(query, conn)
    conn.close()

    return {
        "total_registros": int(stats.loc[0, "total_registros"]),
        "promedio_operaciones": float(stats.loc[0, "promedio_operaciones"]),
        "maximo_operaciones": float(stats.loc[0, "maximo_operaciones"]),
        "minimo_operaciones": float(stats.loc[0, "minimo_operaciones"])
    }


def obtener_aeropuertos():
    conn = get_connection()

    df = pd.read_sql_query(
        "SELECT * FROM operaciones LIMIT 1",
        conn
    )

    conn.close()

    columnas = [
        col for col in df.columns
        if col.startswith("aeropuerto_oaci_")
    ]

    return [
        col.replace("aeropuerto_oaci_", "")
        for col in columnas
    ]
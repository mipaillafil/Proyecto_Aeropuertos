from pathlib import Path
import pandas as pd
import requests


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CSV_ORIGINAL = DATA_DIR / "operaciones_aeropuertos_dirty.csv"
CSV_LIMPIO = DATA_DIR / "operaciones_aeropuertos_clean.csv"

COLUMNAS_ESPERADAS = [
    "mes_id",
    "aeropuerto_oaci",
    "internacional_domestico",
    "cnt_operaciones"
]


def validar_esquema(df: pd.DataFrame) -> None:
    """
    Valida que el dataset contenga las columnas necesarias.
    """
    columnas_faltantes = [
        columna for columna in COLUMNAS_ESPERADAS
        if columna not in df.columns
    ]

    if columnas_faltantes:
        raise ValueError(f"Faltan columnas obligatorias: {columnas_faltantes}")


def extraer_csv() -> pd.DataFrame:
    """
    Extrae datos desde el archivo CSV original.
    """
    if not CSV_ORIGINAL.exists():
        raise FileNotFoundError(f"No existe el archivo: {CSV_ORIGINAL}")

    return pd.read_csv(CSV_ORIGINAL)


def extraer_openmeteo() -> dict:
    """
    Extrae información meteorológica actual desde Open-Meteo.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=-33.45"
        "&longitude=-70.66"
        "&current_weather=true"
    )

    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        return respuesta.json()

    except requests.RequestException:
        return {}


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia, valida e imputa los datos del dataset.
    """
    validar_esquema(df)

    df = df.copy()

    # Limpieza de texto
    columnas_texto = df.select_dtypes(include="object").columns

    for columna in columnas_texto:
        df[columna] = (
            df[columna]
            .astype(str)
            .str.strip()
            .str.upper()
        )

    # Eliminar duplicados
    df = df.drop_duplicates()

    # Conversión de cnt_operaciones a numérico
    df["cnt_operaciones"] = pd.to_numeric(
        df["cnt_operaciones"],
        errors="coerce"
    )

    # Imputación de valores nulos: usar mediana solo en columnas numéricas
    for columna in df.columns:
        if df[columna].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[columna]):
                df[columna] = df[columna].fillna(df[columna].median())
            else:
                modes = df[columna].mode()
                fill_value = modes.iat[0] if not modes.empty else ""
                df[columna] = df[columna].fillna(fill_value)

    # Validación de operaciones negativas
    df = df[df["cnt_operaciones"] >= 0]

    return df


def transformaciones_avanzadas(df: pd.DataFrame) -> None:
    """
    Genera transformaciones avanzadas con Pandas.
    """

    # 1. Agrupación múltiple con varias métricas
    resumen = (
        df.groupby(["mes_id", "aeropuerto_oaci"])
        .agg(
            total_operaciones=("cnt_operaciones", "sum"),
            promedio_operaciones=("cnt_operaciones", "mean"),
            max_operaciones=("cnt_operaciones", "max"),
            min_operaciones=("cnt_operaciones", "min"),
            cantidad_registros=("cnt_operaciones", "count")
        )
        .reset_index()
    )

    resumen.to_csv(DATA_DIR / "resumen_operaciones.csv", index=False)

    # 2. Pivot table por tipo de vuelo
    pivot = pd.pivot_table(
        df,
        values="cnt_operaciones",
        index="aeropuerto_oaci",
        columns="internacional_domestico",
        aggfunc="sum",
        fill_value=0
    )

    pivot.to_csv(DATA_DIR / "pivot_operaciones.csv")

    # 3. Ranking de aeropuertos
    ranking = (
        df.groupby("aeropuerto_oaci")["cnt_operaciones"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    ranking["ranking"] = ranking["cnt_operaciones"].rank(
        ascending=False,
        method="dense"
    )

    ranking.to_csv(DATA_DIR / "ranking_aeropuertos.csv", index=False)

    # 4. Transformación vectorizada
    df["categoria_operacion"] = pd.cut(
        df["cnt_operaciones"],
        bins=[-1, 100, 500, 1000, float("inf")],
        labels=["BAJA", "MEDIA", "ALTA", "MUY ALTA"]
    )

    df.to_csv(DATA_DIR / "operaciones_categorizadas.csv", index=False)


def ejecutar_etl() -> None:
    """
    Ejecuta el pipeline ETL completo.
    """
    try:
        df = extraer_csv()

        # Segunda fuente externa
        clima = extraer_openmeteo()

        df_limpio = limpiar_datos(df)
        transformaciones_avanzadas(df_limpio)

        df_limpio.to_csv(CSV_LIMPIO, index=False)

        print("ETL ejecutado correctamente.")
        print(f"Registros finales: {len(df_limpio)}")
        print(f"Datos climáticos obtenidos: {'Sí' if clima else 'No'}")
        print(f"Archivo limpio guardado en: {CSV_LIMPIO}")

    except Exception as error:
        print(f"Error en el pipeline ETL: {error}")
        raise


if __name__ == "__main__":
    ejecutar_etl()
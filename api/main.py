from fastapi import FastAPI
from database import obtener_datos
from openmeteo import obtener_clima
import pandas as pd
from typing import Optional

app = FastAPI(
    title="API Aeropuertos",
    version="1.0"
)

@app.get("/api/v1/")
def inicio():
    return {"mensaje": "API Sistema Aeroportuario"}

@app.get("/api/v1/estadisticas")
def estadisticas():
    df = obtener_datos()
    return {
        "registros": len(df),
        "promedio_operaciones": float(df["cnt_operaciones"].mean())
    }

@app.get("/api/v1/aeropuertos")
def aeropuertos():
    df = obtener_datos()
    if "aeropuerto" in df.columns:
        return sorted(df["aeropuerto"].dropna().unique().tolist())

    columnas = [
        c
        for c in df.columns
        if c.startswith("aeropuerto_oaci_")
    ]

    return [c.replace("aeropuerto_oaci_", "") for c in columnas]

@app.get("/api/v1/operaciones")
def operaciones(
    aeropuerto: Optional[str] = None,
    min_ops: Optional[float] = None,
    max_ops: Optional[float] = None
):
    df = obtener_datos()
    if aeropuerto:
        df = df[df["aeropuerto"] == aeropuerto]
    if min_ops is not None:
        df = df[df["cnt_operaciones"] >= min_ops]
    if max_ops is not None:
        df = df[df["cnt_operaciones"] <= max_ops]

    if "fecha" in df.columns:
        df["fecha"] = df["fecha"].astype(str)

    return df.to_dict(orient="records")

@app.get("/api/v1/clima")
def clima():
    return obtener_clima()

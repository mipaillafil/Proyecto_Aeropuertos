from fastapi import FastAPI, Response
from api.database import obtener_aeropuertos, obtener_datos, obtener_estadisticas
from api.openmeteo import obtener_clima

app = FastAPI(
    title="API Sistema Aeroportuario",
    version="1.0"
)


@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)


@app.get("/")
def inicio():
    return {
        "mensaje": "API Sistema Aeroportuario funcionando"
    }


@app.get("/api/v1/estadisticas")
def estadisticas():
    return obtener_estadisticas()


@app.get("/api/v1/operaciones")
def operaciones(limit: int = 3000):
    df = obtener_datos(limit)
    return df.to_dict(orient="records")


@app.get("/api/v1/aeropuertos")
def aeropuertos():
    return {
        "aeropuertos": obtener_aeropuertos()
    }


@app.get("/api/v1/clima")
def clima():
    return obtener_clima()
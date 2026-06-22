import requests

def obtener_clima():

    lat = -33.45
    lon = -70.66

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&current_weather=true"
    )

    respuesta = requests.get(url)

    return respuesta.json()
from api.openmeteo import obtener_clima


def test_obtener_clima():
    data = obtener_clima()

    assert data is not None
    assert "current_weather" in data
    assert "temperature" in data["current_weather"]
    assert "windspeed" in data["current_weather"]
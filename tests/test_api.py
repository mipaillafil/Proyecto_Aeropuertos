from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_inicio_api():
    response = client.get("/")
    assert response.status_code == 200
    assert "mensaje" in response.json()


def test_endpoint_estadisticas():
    response = client.get("/api/v1/estadisticas")
    assert response.status_code == 200

    data = response.json()
    assert "total_registros" in data
    assert "promedio_operaciones" in data
    assert data["total_registros"] > 0


def test_endpoint_operaciones():
    response = client.get("/api/v1/operaciones?limit=10")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_endpoint_aeropuertos():
    response = client.get("/api/v1/aeropuertos")
    assert response.status_code == 200

    data = response.json()
    assert "aeropuertos" in data
    assert isinstance(data["aeropuertos"], list)


def test_endpoint_clima():
    response = client.get("/api/v1/clima")
    assert response.status_code == 200

    data = response.json()
    assert "current_weather" in data
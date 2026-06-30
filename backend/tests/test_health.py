"""
Tests del bootstrap de la aplicación.

Verifican que los dos únicos endpoints expuestos en esta iteración
(`/` y `/health`) respondan correctamente.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """`GET /` debe devolver el nombre y la versión de la aplicación."""
    response = client.get("/")

    assert response.status_code == 200
    body = response.json()
    assert body["application"] == "Agentic RAG Platform"
    assert body["version"] == "1.0.0"


def test_health_endpoint() -> None:
    """`GET /health` debe devolver el estado de salud del servicio."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

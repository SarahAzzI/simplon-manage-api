import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_responds():
    """Verify backend is alive."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API Centre de Formation opérationnelle"}

def test_swagger_ui_available():
    """Verify Swagger UI documentation is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger-ui" in response.text.lower()

def test_openapi_spec_available():
    """Verify OpenAPI JSON specification is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "API Centre de Formation — Simplon"

def test_database_connection_via_formations():
    """Verify backend can fetch data from database."""
    response = client.get("/formations/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

def test_database_connection_via_users():
    """Verify backend can fetch users from database."""
    response = client.get("/utilisateurs/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert isinstance(data["items"], list)

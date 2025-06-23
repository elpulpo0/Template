import pytest
from fastapi.testclient import TestClient
from backend.main import create_app

@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client

def test_cors_middleware_configured(app):
    from fastapi.middleware.cors import CORSMiddleware
    middlewares = [m.cls for m in app.user_middleware]
    assert CORSMiddleware in middlewares, "CORS middleware non configuré"

def test_routes_exist(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200

    paths = response.json().get("paths", {}).keys()
    assert any(p.startswith("/health") for p in paths), "Route /health non trouvée"
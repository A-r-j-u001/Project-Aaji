from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_health():
    # Since we don't have a specific health endpoint, we check if the app initializes
    # and 404s on root (which implies the server is running).
    response = client.get("/")
    assert response.status_code == 404

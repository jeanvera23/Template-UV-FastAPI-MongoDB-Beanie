from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "name": "APP Name",
        "version": "0.0.1",
        "description": "Application description"
    }
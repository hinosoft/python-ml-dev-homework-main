from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_recipe():
    response = client.get("/recipes/1/")
    assert response.status_code == 200
    data = response.json()
    assert "recipe" in data
    assert "total_cost" in data
    assert "nutrition" in data

def test_invalid_recipe():
    response = client.get("/recipes/9999/")
    assert response.status_code == 404

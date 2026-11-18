from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "MovieSphere" in response.text
    assert "2026" in response.text

def test_movie_api():
    response = client.get("/api/movies?limit=2")
    assert response.status_code == 200
    assert len(response.json()["movies"]) == 2

def test_2026_starter_movies():
    response = client.get("/api/movies?year=2026&limit=30")
    assert response.status_code == 200
    assert len(response.json()["movies"]) >= 10
    assert all(movie["year"] == "2026" for movie in response.json()["movies"])

def test_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json()["brand"] == "MovieSphere"


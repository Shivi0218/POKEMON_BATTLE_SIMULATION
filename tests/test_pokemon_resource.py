import pytest
from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)

def test_get_pokemon_by_name():
    response = client.get("/api/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json()["name"] == "pikachu"
    assert response.json()["id"] == 25

def test_get_pokemon_by_id():
    response = client.get("/api/pokemon/1")
    assert response.status_code == 200
    assert response.json()["name"] == "bulbasaur"
    assert response.json()["id"] == 1

def test_get_pokemon_not_found():
    response = client.get("/api/pokemon/unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "Pokémon not found"}
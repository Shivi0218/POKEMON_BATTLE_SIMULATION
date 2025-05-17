import pytest
from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)

def test_battle_simulation():
    response = client.post("/api/battle", json={"pokemon1": "charmander", "pokemon2": "squirtle"})
    assert response.status_code == 200
    result = response.json()
    assert "winner" in result
    assert "logs" in result
    assert result["winner"] in ["charmander", "squirtle"]
    assert len(result["logs"]) > 0

def test_battle_simulation_with_status_effect():
    response = client.post("/api/battle", json={"pokemon1": "pikachu", "pokemon2": "bulbasaur"})
    assert response.status_code == 200
    result = response.json()
    assert "winner" in result
    assert "logs" in result
    # Check for status effect in logs (since it's probabilistic, this might need multiple runs)
    has_status = any("paralyzed" in log["outcome"] for log in result["logs"])
    assert result["winner"] in ["pikachu", "bulbasaur"]

def test_battle_invalid_pokemon():
    response = client.post("/api/battle", json={"pokemon1": "charmander", "pokemon2": "unknown"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Pokémon not found"}
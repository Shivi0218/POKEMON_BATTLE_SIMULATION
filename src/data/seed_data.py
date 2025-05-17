import requests
import sqlite3
import json

def fetch_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def init_db():
    conn = sqlite3.connect("src/data/pokemon.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pokemon (
            id INTEGER PRIMARY KEY,
            name TEXT,
            types TEXT,
            stats TEXT,
            abilities TEXT,
            moves TEXT,
            evolutions TEXT
        )
    """)
    conn.commit()
    return conn, cursor

def seed_pokemon(limit=151):  # Gen 1 for simplicity
    conn, cursor = init_db()
    for i in range(1, limit + 1):
        data = fetch_pokemon_data(i)
        if data:
            types = json.dumps([t["type"]["name"] for t in data["types"]])
            stats = json.dumps({s["stat"]["name"]: s["base_stat"] for s in data["stats"]})
            abilities = json.dumps([a["ability"]["name"] for a in data["abilities"]])
            moves = json.dumps([m["move"]["name"] for m in data["moves"]])
            evolutions = json.dumps([])  # Placeholder (extend if needed)
            cursor.execute(
                "INSERT OR REPLACE INTO pokemon (id, name, types, stats, abilities, moves, evolutions) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data["id"], data["name"], types, stats, abilities, moves, evolutions)
            )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_pokemon()
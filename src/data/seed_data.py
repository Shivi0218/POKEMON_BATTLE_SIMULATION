import requests
import sqlite3
import json

def fetch_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_species_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def fetch_evolution_chain(chain_url):
    response = requests.get(chain_url)
    if response.status_code == 200:
        return response.json()
    return None

def get_evolution_names(chain_data):
    evolution_names = []
    
    def extract_evolutions(evolution_data):
        if evolution_data:
            species_name = evolution_data['species']['name']
            evolution_names.append(species_name)
            
            # Process all evolves_to entries
            for evolves_to in evolution_data.get('evolves_to', []):
                extract_evolutions(evolves_to)
    
    # Start with the base chain
    extract_evolutions(chain_data['chain'])
    return evolution_names

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
            # Fetch species data to get evolution chain URL
            species_data = fetch_species_data(i)
            evolution_names = []
            
            if species_data and species_data.get('evolution_chain', {}).get('url'):
                # Fetch and process evolution chain
                chain_data = fetch_evolution_chain(species_data['evolution_chain']['url'])
                if chain_data:
                    evolution_names = get_evolution_names(chain_data)
            
            types = json.dumps([t["type"]["name"] for t in data["types"]])
            stats = json.dumps({s["stat"]["name"]: s["base_stat"] for s in data["stats"]})
            abilities = json.dumps([a["ability"]["name"] for a in data["abilities"]])
            moves = json.dumps([m["move"]["name"] for m in data["moves"]])
            evolutions = json.dumps(evolution_names)
            
            cursor.execute(
                "INSERT OR REPLACE INTO pokemon (id, name, types, stats, abilities, moves, evolutions) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data["id"], data["name"], types, stats, abilities, moves, evolutions)
            )
            print(f"Processed Pokemon #{i}: {data['name']} with evolutions: {evolution_names}")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    seed_pokemon()
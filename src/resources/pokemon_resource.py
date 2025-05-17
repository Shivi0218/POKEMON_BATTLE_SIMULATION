from fastapi import APIRouter, HTTPException
from src.models.pokemon import Pokemon
import sqlite3
import json

router = APIRouter()

def get_db_connection():
    conn = sqlite3.connect("src/data/pokemon.db")
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/pokemon/{identifier}", response_model=Pokemon)
async def get_pokemon(identifier: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM pokemon WHERE id = ? OR name = ?"
    cursor.execute(query, (identifier, identifier.lower()))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return Pokemon(
        id=row["id"],
        name=row["name"],
        types=json.loads(row["types"]),
        stats=json.loads(row["stats"]),
        abilities=json.loads(row["abilities"]),
        moves=json.loads(row["moves"]),
        evolutions=json.loads(row["evolutions"])
    )
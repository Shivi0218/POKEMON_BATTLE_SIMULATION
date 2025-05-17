from fastapi import FastAPI
from src.resources.pokemon_resource import router as pokemon_router
from src.resources.battle_resource import router as battle_router

app = FastAPI(title="Pokémon MCP Server")

app.include_router(pokemon_router, prefix="/api")
app.include_router(battle_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import APIRouter, HTTPException
from src.models.battle import BattleInput, BattleResult
from src.tools.battle_tool import simulate_battle

router = APIRouter()

@router.post("/battle", response_model=BattleResult)
async def battle_pokemon(battle_input: BattleInput):
    try:
        result = await simulate_battle(battle_input)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Battle simulation failed: {str(e)}")
from pydantic import BaseModel
from typing import List

class BattleInput(BaseModel):
    pokemon1: str
    pokemon2: str

class BattleAction(BaseModel):
    turn: int
    action: str
    outcome: str

class BattleResult(BaseModel):
    winner: str
    logs: List[BattleAction]
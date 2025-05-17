from pydantic import BaseModel
from typing import List, Dict

class Pokemon(BaseModel):
    id: int
    name: str
    types: List[str]
    stats: Dict[str, int]
    abilities: List[str]
    moves: List[str]
    evolutions: List[str]
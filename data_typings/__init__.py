from typing import List, TypedDict, Optional, Dict, Literal


class DbData(TypedDict):
    user: str
    password: str
    host: str
    database: str
    dialect: str
    connector: str
    port: Optional[int]
    
    
class BuffAnswer(TypedDict):
    success: str
    possible: List[str]


class Puzzles(TypedDict):
    travel: Dict[str, Literal["safe", "warn", "danger"]]
    pages: Dict[str, str]
    door: Dict[str, str]
    cross: Dict[str, str]
    buffs: BuffAnswer


class BuffClasses(TypedDict):
    apostol: int
    warlock: int
    paladin: int
    crusader: int
    light_inc: int

from typing import TypedDict, Optional, List, Dict


class DbData(TypedDict):
    user: str
    password: str
    host: str
    database: str
    dialect: str
    connector: str
    port: Optional[int]


class PuzzleTravel(TypedDict):
    safe: List[str]
    warn: List[str]
    danger: List[str]

class Puzzles(TypedDict):
    travel: PuzzleTravel
    pages: Dict[str, str]
    door: Dict[str, str]
    cross: Dict[str, str]

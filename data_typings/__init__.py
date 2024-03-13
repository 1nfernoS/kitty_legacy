from typing import TypedDict, Optional, Dict, Literal


class DbData(TypedDict):
    user: str
    password: str
    host: str
    database: str
    dialect: str
    connector: str
    port: Optional[int]

class Puzzles(TypedDict):
    travel: Dict[str, Literal["safe", "warn", "danger"]]
    pages: Dict[str, str]
    door: Dict[str, str]
    cross: Dict[str, str]

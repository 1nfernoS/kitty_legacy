from typing import List, TypedDict, Optional, Dict, Literal

from data_typings.enums import EventPayloadAction


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


class BuffPayload(TypedDict):
    msg_id: int
    chat_id: int
    from_id: int
    buff_id: int
    

class EventPayload(TypedDict):
    action: EventPayloadAction
    data: Optional[BuffPayload]

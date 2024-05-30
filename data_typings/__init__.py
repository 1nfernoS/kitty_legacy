from typing import List, TypedDict, Optional, Dict, Literal

from .enums import EventPayloadAction
from vbml import Pattern

from vkbottle.tools.dev.mini_types.bot import MessageEventMin


class DbData(TypedDict):
    user: str
    password: str
    host: str
    database: str
    dialect: str
    connector: str
    port: Optional[int]


class BuffAnswer(TypedDict):
    critical: Pattern
    success: Pattern
    possible: List[Pattern]


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


class AnnounceRestorePayload(TypedDict):
    note_id: int


class EventPayload(TypedDict):
    action: EventPayloadAction
    data: Optional[BuffPayload | AnnounceRestorePayload]


class CtxBufferData(TypedDict):
    payload: BuffPayload
    event: MessageEventMin


class RemindArgs(TypedDict):
    user_id: int
    peer_id: int
    msg_id: int
    text: str


class CtxStorageData(TypedDict):
    item_id: int
    item_name: str
    count: int


class CtxData(TypedDict):
    buffs: Dict[int, CtxBufferData]
    storage: List[Dict[int, CtxStorageData]]

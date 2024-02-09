from typing import TypedDict, Optional


class DbData(TypedDict):
    user: str
    password: str
    host: str
    database: str
    dialect: str
    connector: str
    port: Optional[int]

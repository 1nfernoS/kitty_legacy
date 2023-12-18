import typing as t


class DbData(t.TypedDict):
    user: str
    password: str
    host: str
    database: str
    dialect: str
    connector: str
    port: t.Optional[int]

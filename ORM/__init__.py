from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from config import db_data

__data_source = f"{db_data['dialect']}+{db_data['connector']}://" \
                f"{db_data['user']}:{db_data['password']}@" \
                f"{db_data['host']}:{db_data['port']}/{db_data['database']}"

__engine = create_engine(__data_source, pool_size=10, max_overflow=20)


class Base(DeclarativeBase):
    pass


def session() -> Session:
    return Session(__engine)


__all__ = ["session", "Base",
           "Item", "Role", "User",
           "BufferType", "BuffCmd", "BuffUser",
           "PuzzleType", "PuzzleAnswer",
           "LogsCommand", "LogsMoney", "LogsItems", "LogsSiege", "LogsElites",
           "Task", "Announcements"]


if __name__ == 'ORM':
    from .user import *
    from .buffer import *
    from .utils import *
    from .logging import *
    from .puzzles import *
    
    Base.metadata.create_all(__engine)
    pass

from typing import Any, Dict, List, Optional, Set, Type, TypeVar

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session
from typing_extensions import Generic

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
           "LogsCommand", "LogsMoney", "LogsItems", "LogsSiege", "LogsElites",
           "Task", "Notes"]

_T = TypeVar("_T", bound=Base)


def check_defaults(t: Generic[_T], defaults: Set[_T]):
    if not all([isinstance(d, t) for d in defaults]):
        raise TypeError
    
    with session() as s:
        rows: Optional[List[t]] = s.query(t).all()
        for row in defaults:
            if row not in rows:
                s.add(row)
        s.commit()


if __name__ == 'ORM':
    from .user import *
    from .buffer import *
    from .utils import *
    from .logging import *
    
    Base.metadata.create_all(__engine)
    
    _defaults: Dict[_T, Set[_T]] = {
        # int: {1, 2, 1, 3},
        Role: DEFAULT_ROLES,
        BufferType: DEFAULT_BUFFER_TYPES,
        BuffCmd: DEFAULT_BUFFER_COMMANDS,
        BuffTypeCmd: DEFAULT_BUFFER_TYPE_COMMANDS
    }
    
    for obj in _defaults:
        check_defaults(obj, _defaults[obj])
    pass

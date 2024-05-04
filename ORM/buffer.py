from typing import List

from sqlalchemy import ForeignKey, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ORM import Base, session

__all__ = ["BufferType", "BuffCmd", "BuffTypeCmd", "BuffUser"]


class BufferType(Base):
    __tablename__ = 'buffer_type'
    
    buff_type_id: Mapped[int] = mapped_column(ForeignKey('item.id'), primary_key=True)
    buff_type_name: Mapped[str] = mapped_column(String(127))
    
    buff_users: Mapped[List["BuffUser"]] = relationship(back_populates='buff_user_type')
    buff_commands: Mapped[List["BuffCmd"]] = relationship(secondary='buff_type_cmd', back_populates='buff_cmd_type')
    
    def __str__(self):
        return f"<BufferType {self.buff_type_id}: {self.buff_type_name}>"
    
    def __repr__(self):
        return f"<BufferType {self.buff_type_id}: {self.buff_type_name}>"


class BuffCmd(Base):
    __tablename__ = 'buff_cmd'
    
    buff_cmd_id: Mapped[int] = mapped_column(primary_key=True)
    buff_cmd_text: Mapped[str] = mapped_column(String(127))
    
    buff_cmd_type: Mapped[BufferType] = relationship(secondary='buff_type_cmd', back_populates='buff_commands',
                                                     viewonly=True)
    
    def __str__(self):
        return f"<BuffCmd {self.buff_cmd_id}: {self.buff_cmd_text}>"
    
    def __repr__(self):
        return f"<BuffCmd {self.buff_cmd_id}: {self.buff_cmd_text}>"


# noinspection PyTypeChecker
class BuffUser(Base):
    __tablename__ = 'buff_user'
    
    buff_user_id: Mapped[int] = mapped_column(primary_key=True)
    buff_user_is_active: Mapped[bool]
    buff_user_profile_key: Mapped[str] = mapped_column(String(32))
    buff_user_token: Mapped[str] = mapped_column(String(255))
    buff_type_id: Mapped[int] = mapped_column(ForeignKey(BufferType.buff_type_id))
    buff_user_race1: Mapped[int]
    buff_user_race2: Mapped[int]
    buff_user_chat_id: Mapped[int]
    
    buff_user_type: Mapped[BufferType] = relationship(back_populates='buff_users', viewonly=True)
    
    def __init__(self, user_id: int, is_active: bool, profile_key: str, token: str,
                 type_id: int, race1: int, race2: int, chat_id: int):
        super().__init__()
        self.buff_user_id = user_id
        self.buff_user_is_active = is_active
        self.buff_user_profile_key = profile_key
        self.buff_user_token = token
        self.buff_type_id = type_id
        self.buff_user_race1 = race1
        self.buff_user_race2 = race2
        self.buff_user_chat_id = chat_id
        return
    
    def __str__(self):
        return f"<BuffUser {self.buff_user_id}: {self.buff_type_id}>"
    
    def __repr__(self):
        return f"<BuffUser {self.buff_user_id}: {self.buff_type_id}>"


class BuffTypeCmd(Base):
    __tablename__ = 'buff_type_cmd'
    
    buff_type_id: Mapped[int] = mapped_column(ForeignKey(BufferType.buff_type_id), primary_key=True)
    buff_cmd_id: Mapped[int] = mapped_column(ForeignKey(BuffCmd.buff_cmd_id), primary_key=True)


# noinspection PyUnusedLocal
@event.listens_for(BuffCmd.__table__, 'after_create')
def default_commands(*a, **kw):
    with session() as s:
        s.add(BuffCmd(buff_cmd_id=1, buff_cmd_text="Очищение"))
        s.add(BuffCmd(buff_cmd_id=2, buff_cmd_text="Проклятие боли"))
        s.add(BuffCmd(buff_cmd_id=3, buff_cmd_text="Проклятие неудачи"))
        s.add(BuffCmd(buff_cmd_id=4, buff_cmd_text="Проклятие добычи"))
        s.add(BuffCmd(buff_cmd_id=5, buff_cmd_text="Очищение огнем"))
        s.add(BuffCmd(buff_cmd_id=6, buff_cmd_text="Очищение светом"))
        s.add(BuffCmd(buff_cmd_id=7, buff_cmd_text="Благословение атаки"))
        s.add(BuffCmd(buff_cmd_id=8, buff_cmd_text="Благословение защиты"))
        s.add(BuffCmd(buff_cmd_id=9, buff_cmd_text="Благословение удачи"))
        s.add(BuffCmd(buff_cmd_id=10, buff_cmd_text="Благословение race1"))
        s.add(BuffCmd(buff_cmd_id=11, buff_cmd_text="Благословение race2"))
        s.add(BuffCmd(buff_cmd_id=12, buff_cmd_text="Благословение зимы"))
        s.commit()


# noinspection PyUnusedLocal
@event.listens_for(BufferType.__table__, "after_create")
def default_buffer_types(*a, **kw):
    with session() as s:
        s.add(BufferType(buff_type_id=14088, buff_type_name="Паладин"))
        s.add(BufferType(buff_type_id=14093, buff_type_name="Чернокнижник"))
        s.add(BufferType(buff_type_id=14256, buff_type_name="Паладин Крестоносец"))
        s.add(BufferType(buff_type_id=14257, buff_type_name="Паладин Воплощение_света"))
        s.add(BufferType(buff_type_id=14264, buff_type_name="Апостол"))
        s.commit()


# noinspection PyUnusedLocal
@event.listens_for(BuffTypeCmd.__table__, "after_create")
def default_buffer_type_cmd(*a, **kw):
    with session() as s:
        s.add(BuffTypeCmd(buff_type_id=14088, buff_cmd_id=1))
        s.add(BuffTypeCmd(buff_type_id=14093, buff_cmd_id=2))
        s.add(BuffTypeCmd(buff_type_id=14093, buff_cmd_id=3))
        s.add(BuffTypeCmd(buff_type_id=14093, buff_cmd_id=4))
        s.add(BuffTypeCmd(buff_type_id=14256, buff_cmd_id=1))
        s.add(BuffTypeCmd(buff_type_id=14256, buff_cmd_id=5))
        s.add(BuffTypeCmd(buff_type_id=14257, buff_cmd_id=1))
        s.add(BuffTypeCmd(buff_type_id=14257, buff_cmd_id=6))
        s.add(BuffTypeCmd(buff_type_id=14264, buff_cmd_id=7))
        s.add(BuffTypeCmd(buff_type_id=14264, buff_cmd_id=8))
        s.add(BuffTypeCmd(buff_type_id=14264, buff_cmd_id=9))
        s.add(BuffTypeCmd(buff_type_id=14264, buff_cmd_id=10))
        s.add(BuffTypeCmd(buff_type_id=14264, buff_cmd_id=11))
        s.add(BuffTypeCmd(buff_type_id=14264, buff_cmd_id=12))
        s.commit()

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ORM import Base, session

from utils import datetime as dt


__all__ = ["LogsType", "Logs", "CommandLogs"]

class LogsType(Base):

    __tablename__ = 'logs_type'

    logs_type_id: Mapped[int] = mapped_column(primary_key=True)
    logs_type_name: Mapped[str]

    def register(self):
        with session() as s:
            s.add(self)
            s.commit()
        return

    def __str__(self):
        return f"<LogsType {self.logs_type_id}: {self.logs_type_name}>"

    def __repr__(self):
        return f"<LogsType {self.logs_type_id}: {self.logs_type_name}>"


class Logs(Base):
    __tablename__ = 'logs'

    logs_entry_id: Mapped[int] = mapped_column(primary_key=True)
    logs_timestamp: Mapped[datetime]
    logs_type_id: Mapped[int]
    logs_user_id: Mapped[int]
    logs_msg_text: Mapped[str]
    logs_on_user_id: Mapped[int]
    logs_on_message: Mapped[str]

    def make_record(self):
        with session() as s:
            s.add(self)
            s.commit()
        return

    def __str__(self):
        return f"<Logs {self.logs_user_id}: {self.logs_msg_text}>"

    def __repr__(self):
        return f"<Logs {self.logs_user_id}: {self.logs_msg_text}>"

class CommandLogs(Base):
    __tablename__ = 'command_logs'

    logs_id: Mapped[int] = mapped_column(primary_key=True)
    logs_timestamp: Mapped[datetime] = mapped_column(default=dt.now())
    logs_command: Mapped[str] = mapped_column(String(31), nullable=False, comment="name of command def")
    logs_user_id: Mapped[int] = mapped_column(nullable=False)
    logs_msg_text: Mapped[str] = mapped_column(String(255), nullable=False)
    logs_on_user_id: Mapped[int] = mapped_column(nullable=True)
    logs_on_message: Mapped[str] = mapped_column(String(255), nullable=True)

    def make_record(self):
        with session() as s:
            s.add(self)
            s.commit()
        return

    def __str__(self):
        return f"<Logs {self.logs_user_id}: {self.logs_msg_text}>"

    def __repr__(self):
        return f"<Logs {self.logs_user_id}: {self.logs_msg_text}>"


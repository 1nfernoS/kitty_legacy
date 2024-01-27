from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column

from ORM import Base, session

from config import TZ


__all__ = ["Task", "Notes"]


class Task(Base):

    __tablename__ = 'tasks'

    task_id: Mapped[int] = mapped_column(primary_key=True)
    task_time_at: Mapped[datetime]
    task_exec_target: Mapped[str]
    task_args: Mapped[str]
    task_created_at: Mapped[datetime]
    task_active: Mapped[bool] = mapped_column(default=True)
    task_regular: Mapped[bool] = mapped_column(default=False)

    def add(self):
        """
        Adds task in database
        """
        with session() as s:
            s.add(self)
            s.commit()
            return

    def __str__(self):
        return f"<Task({int(self.task_regular)}) {self.task_exec_target}<{self.task_time_at}>: [{self.task_args}]>"

    def __repr__(self):
        return f"<Task({int(self.task_regular)}) {self.task_exec_target}<{self.task_time_at}>: [{self.task_args}]>"


class Notes(Base):
    __tablename__ = 'notes'

    note_id: Mapped[int] = mapped_column(primary_key=True)
    note_author: Mapped[int]
    note_text: Mapped[str]
    expires_in: Mapped[datetime]
    is_active: Mapped[bool]

    def __init__(self, author: int, text: str, expires: datetime = datetime.utcnow() + timedelta(hours=168 + TZ),
                 active: bool = True):
        self.note_author = author
        self.note_text = text
        self.expires_in = expires
        self.is_active = active
        return

    def save(self):
        with session() as s:
            s.add(self)
            s.commit()

    def restore(self):
        self.is_active = True
        self.expires_in = datetime.utcnow() + timedelta(hours=168+3)
        self.save()
        return

    def remove(self):
        self.is_active = False
        self.save()
        return

    def __str__(self):
        return f"<Note({int(self.note_author)}): {self.note_text[:25]}<{self.expires_in}]>"

    def __repr__(self):
        return f"<Note({int(self.note_author)}): {self.note_text[:25]}<{self.expires_in}]>"

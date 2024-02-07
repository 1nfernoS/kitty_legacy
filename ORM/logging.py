from datetime import datetime

from sqlalchemy import String, ForeignKey, event
from sqlalchemy.orm import Mapped, mapped_column

from . import Base, session

from data_typings.enums import ChangeMoneyAction, ItemAction

from utils.datetime import now

__all__ = ("LogsSiege", "LogsElites", "LogsItems", "LogsMoney", "LogsCommand")


class _LogsBase:
    log_id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=now())
    user_id: Mapped[int] = mapped_column(nullable=False)

    def __init__(self, user_id: int):
        self.timestamp = now()
        self.user_id = user_id
        return

    def make_log(self):
        with session() as s:
            s.add(self)
            s.commit()


class LogsSiege(_LogsBase, Base):
    __tablename__ = 'logs_siege'

    guild: Mapped[str] = mapped_column(String(63), nullable=False, default=now())

    def __init__(self, user_id: int, guild: str):
        self.guild = guild
        super().__init__(user_id)

    def __str__(self):
        return f"Siege report {self.user_id}: {self.guild}"

    def __repr__(self):
        return f"<LogsSiege {self.timestamp} ({self.user_id})>"


class LogsElites(_LogsBase, Base):
    __tablename__ = 'logs_elites'

    count: Mapped[int] = mapped_column(nullable=False)

    def __init__(self, user_id: int, count: int):
        self.count = count
        super().__init__(user_id)

    def __str__(self):
        return f"Elites report {self.user_id}: {self.count}"

    def __repr__(self):
        return f"<LogsElites {self.timestamp} ({self.user_id}: {self.count})>"


class LogsItems(_LogsBase, Base):
    __tablename__ = 'logs_items'

    action: Mapped[str] = mapped_column(ForeignKey('logs_item_actions.action_type'),
                                        nullable=False)
    user_to: Mapped[int] = mapped_column(nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'), nullable=False)
    count: Mapped[int] = mapped_column(nullable=False, default=1)

    def __init__(self, user_id: int, action: ItemAction, user_to: int, item_id: int, count: int):
        self.action = action.value
        self.user_to = user_to
        self.item_id = item_id
        self.count = count
        super().__init__(user_id)

    def __str__(self):
        return f"Item transfer {self.item_id}({self.count})"

    def __repr__(self):
        return f"<LogsItems [{self.timestamp}] {self.action} {self.user_to} - {self.item_id} ({self.count})>"


class LogsMoney(_LogsBase, Base):
    __tablename__ = 'logs_money'

    action: Mapped[str] = mapped_column(ForeignKey('logs_money_action.action_type'),
                                        nullable=False)
    count: Mapped[int] = mapped_column(nullable=False, default=1)
    user_change: Mapped[int] = mapped_column(nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=True, default='Changed in DB')

    def __init__(self, user_id: int, action: ChangeMoneyAction, count: int, user_change: int, reason: str = None):
        self.action = action.value
        self.count = count
        self.user_change = user_change
        self.reason = reason
        super().__init__(user_id)

    def __str__(self):
        return f"Money balance change {self.user_id}({self.count})"

    def __repr__(self):
        return f"<LogsMoney [{self.timestamp}] {self.user_id} ({self.action} {self.count})>"


class LogsCommand(_LogsBase, Base):
    __tablename__ = 'logs_command'

    command: Mapped[str] = mapped_column(String(127), nullable=False)
    command_text: Mapped[str] = mapped_column(String(255), nullable=False)
    on_user: Mapped[int] = mapped_column(nullable=False)
    on_user_text: Mapped[str] = mapped_column(String(255), nullable=True)

    def __init__(self, user_id: int, command: str, command_text: str, on_user: int = None, on_user_text: str = None):
        self.command = command
        self.command_text = command_text
        self.on_user = on_user
        self.on_user_text = on_user_text
        super().__init__(user_id)

    def __str__(self):
        return f"Command {self.command} from {self.user_id})"

    def __repr__(self):
        return f"<LogsCommand [{self.timestamp}] {self.user_id} ({self.command_text})>"


class __LogsItemsAction(Base):
    __tablename__ = 'logs_item_actions'

    action_type: Mapped[str] = mapped_column(String(63), primary_key=True)


class __LogsMoneyAction(Base):
    __tablename__ = 'logs_money_action'

    action_type: Mapped[str] = mapped_column(String(63), primary_key=True)


@event.listens_for(__LogsMoneyAction.__table__, 'after_create')
def default_money_action(*a, **kw):
    with session() as s:
        for act in ChangeMoneyAction:
            s.add(__LogsMoneyAction(action_type=act.value))
        s.commit()


@event.listens_for(__LogsItemsAction.__table__, 'after_create')
def default_item_action(*a, **kw):
    with session() as s:
        for act in ItemAction:
            s.add(__LogsItemsAction(action_type=act.value))
        s.commit()

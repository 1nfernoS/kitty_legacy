from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


from utils.datetime import now


__all__ = ("LogsSiege", "LogsElites")


class _LogsBase(DeclarativeBase):
    log_id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    user_id: Mapped[int] = mapped_column(nullable=False)


class LogsSiege(_LogsBase):

    __tablename__ = 'logs_siege'

    guild: Mapped[str] = mapped_column(String(63), nullable=False, default=now())

    def __str__(self):
        return f"Siege report {self.user_id}: {self.guild}"

    def __repr__(self):
        return f"<LogsSiege {self.timestamp} ({self.user_id})>"


class LogsElites(_LogsBase):

    __tablename__ = 'logs_elites'

    count: Mapped[int] = mapped_column(nullable=False)

    def __str__(self):
        return f"Elites report {self.user_id}: {self.count}"

    def __repr__(self):
        return f"<LogsElites {self.timestamp} ({self.user_id}: {self.count})>"

class __LogsItemsAction(_LogsBase):

    __tablename__ = 'logs_item_actions'

    action_type: Mapped[str] = mapped_column(primary_key=True)


class LogsItems(_LogsBase):

    __tablename__ = 'logs_items'

    action: Mapped[str] = mapped_column(ForeignKey('logs_item_actions.action_type'),
                                        nullable=False)
    user_to: Mapped[int] = mapped_column(nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'), nullable=False)
    count: Mapped[int] = mapped_column(nullable=False, default=1)

    def __str__(self):
        return f"Item transfer {self.item_id}({self.count})"

    def __repr__(self):
        return f"<LogsItems [{self.timestamp}] {self.action} {self.user_to} - {self.item_id} ({self.count})>"

class __LogsMoneyAction(_LogsBase):

    __tablename__ = 'logs_money_action'

    action_type: Mapped[str] = mapped_column(primary_key=True)


class LogsMoney(_LogsBase):

    __tablename__ = 'logs_money'

    action: Mapped[str] = mapped_column(ForeignKey('logs_money_action.action_type'),
                                        nullable=False)
    count: Mapped[int] = mapped_column(nullable=False, default=1)
    user_change: Mapped[int] = mapped_column(nullable=False)
    reason: Mapped[str] = mapped_column(String(255), nullable=True, default='Changed in DB')

    def __str__(self):
        return f"Money balance change {self.user_id}({self.count})"

    def __repr__(self):
        return f"<LogsMoney [{self.timestamp}] {self.user_id} ({self.action} {self.count})>"


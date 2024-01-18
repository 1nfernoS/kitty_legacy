from datetime import datetime
from typing import List, Dict

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ORM import Base, session

__all__ = ["Item", "Role", "User", "Equipment"]


class Item(Base):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    has_price: Mapped[bool]

    item_users: Mapped[List["User"]] = relationship(secondary='equipment', back_populates='user_items',
                                                        viewonly=True)

    def __init__(self, item_id: int, name: str, has_price: bool = False):
        super().__init__()
        self.id = item_id
        self.name = name
        self.has_price = has_price
        return

    def __str__(self):
        return f'<Item {self.id}: {self.name}>'

    def __repr__(self):
        return f'<Item {self.id}: {self.name}>'


class Role(Base):
    __tablename__ = 'role'

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str]
    role_basic: Mapped[bool]
    role_get_buff: Mapped[bool]
    role_check_stats: Mapped[bool]
    role_balance: Mapped[bool]
    role_profile_app_check: Mapped[bool]
    role_change_balance: Mapped[bool]
    role_moderate: Mapped[bool]
    role_kick: Mapped[bool]
    role_check_all_balance: Mapped[bool]
    role_withdraw_bill: Mapped[bool]
    role_change_role: Mapped[bool]
    role_utils: Mapped[bool]
    role_take_money: Mapped[bool]
    role_take_books: Mapped[bool]
    role_take_ingredients: Mapped[bool]

    role_users: Mapped[List["User"]] = relationship(back_populates='user_role', viewonly=True)

    def __init__(self, role_id: int, name: str, can_basic: bool = False, can_get_buff: bool = False,
                 can_check_stats: bool = False, can_balance: bool = False, can_profile_app_check: bool = False,
                 can_change_balance: bool = False, can_moderate: bool = False, can_kick: bool = False,
                 can_check_all_balance: bool = False, can_withdraw_bill: bool = False, can_change_role: bool = False,
                 can_utils: bool = False, can_take_money: bool = False, can_take_books: bool = False,
                 can_take_ingredients: bool = False):
        super().__init__()
        if role_id < 0:
            raise ValueError
        self.role_id = role_id
        self.role_name = name
        self.role_basic = can_basic
        self.role_get_buff = can_get_buff
        self.role_check_stats = can_check_stats
        self.role_balance = can_balance
        self.role_profile_app_check = can_profile_app_check
        self.role_change_balance = can_change_balance
        self.role_moderate = can_moderate
        self.role_kick = can_kick
        self.role_check_all_balance = can_check_all_balance
        self.role_withdraw_bill = can_withdraw_bill
        self.role_change_role = can_change_role
        self.role_utils = can_utils
        self.role_take_money = can_take_money
        self.role_take_books = can_take_books
        self.role_take_ingredients = can_take_ingredients
        return

    def role_level_access(self) -> int:
        return int(f"{self.role_basic}{self.role_get_buff}{self.role_check_stats}{self.role_balance}"
                   f"{self.role_profile_app_check}{self.role_change_balance}{self.role_moderate}"
                   f"{self.role_kick}{self.role_check_all_balance}{self.role_withdraw_bill}"
                   f"{self.role_change_role}{self.role_utils}{self.role_take_money}"
                   f"{self.role_take_books}{self.role_take_ingredients}", 2)

    def bin_access(self) -> str:
        return bin(self.role_level_access())[2:]

    @staticmethod
    def get_guild_roles() -> List["Role"]:
        guild_roles = ['creator', 'leader',
                       'paymaster', 'librarian',
                       'captain', 'officer',
                       'guild_member']
        with session() as s:
            return s.query(Role).filter(Role.role_name.in_(guild_roles)).all()

    @staticmethod
    def leader_role() -> "Role":
        with session() as s:
            return s.query(Role).filter(Role.role_name == 'leader').first()

    @staticmethod
    def captain_role() -> "Role":
        with session() as s:
            return s.query(Role).filter(Role.role_name == 'captain').first()

    @staticmethod
    def officer_role() -> "Role":
        with session() as s:
            return s.query(Role).filter(Role.role_name == 'officer').first()

    @staticmethod
    def guild_role() -> "Role":
        with session() as s:
            return s.query(Role).filter(Role.role_name == 'guild_member').first()

    @staticmethod
    def newbie_role() -> "Role":
        with session() as s:
            return s.query(Role).filter(Role.role_name == 'guild_newbie').first()

    @staticmethod
    def guest_role() -> "Role":
        with session() as s:
            return s.query(Role).filter(Role.role_name == 'guild_guests').first()

    @staticmethod
    def other_role() -> "Role":
        with session() as s:
            return s.query(Role).filter(Role.role_name == 'others').first()

    @staticmethod
    def ban_role() -> "Role":
        with session() as s:
            return s.query(Role).filter(Role.role_name == 'blacklist').first()

    def __eq__(self, other: "Role"):
        if not isinstance(other, Role):
            return False
        return self.role_id == other.role_id

    def __str__(self):
        return f"<Role {self.role_id}: {self.role_name} ({self.bin_access()})>"

    def __repr__(self):
        return f"<Role {self.role_id}: {self.role_name} ({self.bin_access()})>"


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    class_id: Mapped[int]
    stat_level: Mapped[int]
    stat_attack: Mapped[int]
    stat_defence: Mapped[int]
    stat_strength: Mapped[int]
    stat_agility: Mapped[int]
    stat_endurance: Mapped[int]
    stat_luck: Mapped[int]
    stat_accuracy: Mapped[int]
    stat_concentration: Mapped[int]
    update_profile: Mapped[datetime]
    role_id: Mapped[int] = mapped_column(ForeignKey('role.role_id'))
    profile_key: Mapped[str]
    balance: Mapped[int]
    update_balance: Mapped[datetime]

    user_items: Mapped[List["Item"]] = relationship(secondary='equipment', back_populates='item_users')
    user_role: Mapped["Role"] = relationship(back_populates='role_users', viewonly=True)

    def __repr__(self):
        return f'<User {self.user_id} ({self.role_id})>'

    def __str__(self):
        return f'{self.user_id} ({self.user_role.role_name})'


class Equipment(Base):
    __tablename__ = 'equipment'

    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey(Item.id), primary_key=True)

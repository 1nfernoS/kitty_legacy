from datetime import datetime
from typing import List

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ORM import Base

from utils.datetime import now

__all__ = ["Item", "Role", "RoleGroup", "User", "Access"]


class Item(Base):
    __tablename__ = 'item'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(127))
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


class RoleGroup(Base):
    __tablename__ = 'role_group'

    group_name: Mapped[str] = mapped_column(String(127), primary_key=True)
    
    group_roles: Mapped[List["Role"]] = relationship(secondary='role_role_group', viewonly=True)
    
    def __str__(self):
        return f'<RoleGroup {self.group_name}>'
    
    def __repr__(self):
        return f'<RoleGroup {self.group_name}>'


class Role(Base):
    __tablename__ = 'role'

    name: Mapped[str] = mapped_column(String(127), primary_key=True)
    role_group: Mapped[str] = mapped_column(ForeignKey(RoleGroup.group_name), nullable=True)
    
    accesses: Mapped[List["RoleAccess"]] = relationship(secondary='role_access', back_populates='roles')
    role_users: Mapped[List["User"]] = relationship(back_populates='user_role', viewonly=True)
    
    def __str__(self):
        return f"<Role {self.name}>"
    
    def __repr__(self):
        return f"<Role {self.name}>"


class Access(Base):
    __tablename__ = 'access'
    
    access_name: Mapped[str] = mapped_column(String(127), primary_key=True)

    roles: Mapped[List["Role"]] = relationship(secondary='role_access', back_populates='accesses')

    def __str__(self):
        return f'<{self.access_name} Access>'
    
    def __repr__(self):
        return f'<Access {self.access_name}>'


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
    role_name: Mapped[str] = mapped_column(ForeignKey('role.name'))
    profile_key: Mapped[str] = mapped_column(String(32), nullable=True)
    balance: Mapped[int] = mapped_column(default=0)
    update_balance: Mapped[datetime] = mapped_column(default=now())
    
    user_items: Mapped[List["Item"]] = relationship(secondary='equipment', back_populates='item_users')
    user_role: Mapped["Role"] = relationship(back_populates='role_users', viewonly=True)
    
    def __repr__(self):
        return f'<User {self.user_id} ({self.role_name})>'
    
    def __str__(self):
        return f'{self.user_id} ({self.user_role.role_name})'


class __Equipment(Base):
    __tablename__ = 'equipment'
    
    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id), primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey(Item.id), primary_key=True)


class __RoleGroupRole(Base):
    __tablename__ = 'role_role_group'
    
    role_group: Mapped[str] = mapped_column(ForeignKey(RoleGroup.group_name), primary_key=True)
    role: Mapped[str] = mapped_column(ForeignKey(Role.name), primary_key=True)


class __RoleAccess(Base):
    __tablename__ = 'role_access'
    
    role: Mapped[str] = mapped_column(ForeignKey(Role.name), primary_key=True)
    access: Mapped[str] = mapped_column(ForeignKey(Access.access_name), primary_key=True)
    granted: Mapped[bool] = mapped_column(Boolean(), default=False)

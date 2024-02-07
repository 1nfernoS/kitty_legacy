from datetime import datetime
from typing import List

from sqlalchemy import Boolean, ForeignKey, String, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ORM import Base, session

from utils.datetime import now

__all__ = ["Item", "Role", "User"]


class Item(Base):
    __tablename__ = 'item'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(127))
    has_price: Mapped[bool]
    
    item_users: Mapped[List["User"]] = relationship(secondary='equipment', back_populates='user_items',
                                                    viewonly=True)
    
    def __str__(self):
        return f'<Item {self.id}: {self.name}>'
    
    def __repr__(self):
        return f'<Item {self.id}: {self.name}>'


class Role(Base):
    __tablename__ = 'role'
    
    name: Mapped[str] = mapped_column(String(127), primary_key=True)
    alias: Mapped[str] = mapped_column(String(63), nullable=False)
    
    bot_access: Mapped[bool] = mapped_column(Boolean, default=False)
    admin_utils: Mapped[bool] = mapped_column(Boolean, default=False)
    moderator: Mapped[bool] = mapped_column(Boolean, default=False)
    change_role: Mapped[bool] = mapped_column(Boolean, default=False)
    change_balance: Mapped[bool] = mapped_column(Boolean, default=False)
    balance_access: Mapped[bool] = mapped_column(Boolean, default=False)
    profile_app: Mapped[bool] = mapped_column(Boolean, default=False)
    wallet: Mapped[bool] = mapped_column(Boolean, default=False)
    take_money: Mapped[bool] = mapped_column(Boolean, default=False)
    take_books: Mapped[bool] = mapped_column(Boolean, default=False)
    take_ingredients: Mapped[bool] = mapped_column(Boolean, default=False)
    take_buffs: Mapped[bool] = mapped_column(Boolean, default=False)
    stats_access: Mapped[bool] = mapped_column(Boolean, default=False)
    
    role_users: Mapped[List["User"]] = relationship(back_populates='user_role', viewonly=True)
    
    def __str__(self):
        return f"<Role {self.name}>"
    
    def __repr__(self):
        return f"<Role {self.name}>"


class User(Base):
    __tablename__ = 'users'
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    class_id: Mapped[int] = mapped_column(default=None, nullable=True)
    stat_level: Mapped[int] = mapped_column(default=0)
    stat_attack: Mapped[int] = mapped_column(default=0)
    stat_defence: Mapped[int] = mapped_column(default=0)
    stat_strength: Mapped[int] = mapped_column(default=0)
    stat_agility: Mapped[int] = mapped_column(default=0)
    stat_endurance: Mapped[int] = mapped_column(default=0)
    stat_luck: Mapped[int] = mapped_column(default=0)
    stat_accuracy: Mapped[int] = mapped_column(default=0)
    stat_concentration: Mapped[int] = mapped_column(default=0)
    update_profile: Mapped[datetime] = mapped_column(default=now())
    role_name: Mapped[str] = mapped_column(ForeignKey('role.name'), default='other')
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


@event.listens_for(Role.__table__, 'after_create')
def default_roles(*a, **kw):
    with session() as s:
        s.add(Role(name="creator", alias="создатель",
                   bot_access=True,
                   admin_utils=True,
                   moderator=True,
                   change_role=True,
                   change_balance=True,
                   balance_access=True,
                   profile_app=True,
                   wallet=True,
                   take_money=True,
                   take_books=True,
                   take_ingredients=True,
                   take_buffs=True,
                   stats_access=True
                   ))
              
        s.add(Role(name="leader", alias="лидер",
                   bot_access=True,
                   admin_utils=False,
                   moderator=True,
                   change_role=True,
                   change_balance=True,
                   balance_access=True,
                   profile_app=True,
                   wallet=True,
                   take_money=True,
                   take_books=True,
                   take_ingredients=True,
                   take_buffs=True,
                   stats_access=True
                   ))
        
        s.add(Role(name="captain", alias="капитан",
                   bot_access=True,
                   admin_utils=False,
                   moderator=True,
                   change_role=True,
                   change_balance=True,
                   balance_access=True,
                   profile_app=True,
                   wallet=True,
                   take_money=True,
                   take_books=True,
                   take_ingredients=True,
                   take_buffs=True,
                   stats_access=True
                   ))
        
        s.add(Role(name="officer", alias="офицер",
                   bot_access=True,
                   admin_utils=False,
                   moderator=True,
                   change_role=False,
                   change_balance=False,
                   balance_access=True,
                   profile_app=True,
                   wallet=True,
                   take_money=True,
                   take_books=True,
                   take_ingredients=True,
                   take_buffs=True,
                   stats_access=True
                   ))
        
        s.add(Role(name="guild", alias="согильдиец",
                   bot_access=True,
                   admin_utils=False,
                   moderator=False,
                   change_role=False,
                   change_balance=False,
                   balance_access=False,
                   profile_app=True,
                   wallet=True,
                   take_money=True,
                   take_books=True,
                   take_ingredients=True,
                   take_buffs=True,
                   stats_access=True))
        
        s.add(Role(name="newbie", alias="новичок",
                   bot_access=True,
                   admin_utils=False,
                   moderator=False,
                   change_role=False,
                   change_balance=False,
                   balance_access=False,
                   profile_app=False,
                   wallet=True,
                   take_money=False,
                   take_books=False,
                   take_ingredients=True,
                   take_buffs=True,
                   stats_access=True))
        
        s.add(Role(name="guest", alias="гость гильдии",
                   bot_access=True,
                   admin_utils=False,
                   moderator=False,
                   change_role=False,
                   change_balance=False,
                   balance_access=False,
                   profile_app=False,
                   wallet=False,
                   take_money=False,
                   take_books=False,
                   take_ingredients=False,
                   take_buffs=True,
                   stats_access=True))
        
        s.add(Role(name="other", alias="неизвестный",
                   bot_access=True,
                   admin_utils=False,
                   moderator=False,
                   change_role=False,
                   change_balance=False,
                   balance_access=False,
                   profile_app=False,
                   wallet=False,
                   take_money=False,
                   take_books=False,
                   take_ingredients=False,
                   take_buffs=False,
                   stats_access=False))
        
        s.add(Role(name="blacklist", alias="бан",
                   bot_access=False,
                   admin_utils=False,
                   moderator=False,
                   change_role=False,
                   change_balance=False,
                   balance_access=False,
                   profile_app=False,
                   wallet=False,
                   take_money=False,
                   take_books=False,
                   take_ingredients=False,
                   take_buffs=False,
                   stats_access=False
                   ))
        s.commit()


@event.listens_for(Item.__table__, "after_create")
def default_items(*a, **kw):
    with open('ORM/data/items.json') as f:
        import json
        items = json.loads(f.read())
    with session() as s:
        for item in items:
            s.add(Item(id=item, name=items[item]['name'], has_price=items[item]['sell']))
        s.commit()
        
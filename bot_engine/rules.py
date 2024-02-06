from collections.abc import Sequence

from vkbottle.dispatch.rules import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from data_typings.enums import RoleAccess


class WhiteListRule(ABCRule[BaseMessageMin]):
    """
    Rule to check from where comes message.
    True if user not in ignore_users and chat in allowed_chats
    """
    def __init__(self,
                 ignore_users: Sequence[int],
                 allowed_chats: Sequence[int]):
        self.ignore_users = ignore_users
        self.allowed_chats = allowed_chats
        return

    async def check(self, event: BaseMessageMin) -> bool:
        return event.peer_id - 2e9 in self.allowed_chats \
            if event.peer_id > 2e9 \
            else event.peer_id not in self.ignore_users


class AccessRule(ABCRule[BaseMessageMin]):
    def __init__(self, require_access: RoleAccess):
        self.require = require_access.value
        return
    
    async def check(self, event: BaseMessageMin) -> bool:
        if event.from_id < 0:
            return False
        from ORM import session, User, Role
        with session() as s:
            user: User | None = s.query(User).filter(User.user_id == event.from_id).first()
            if not user:
                s.add(User(user_id=event.from_id))
                s.commit()
                user: User | None = s.query(User).filter(User.user_id == event.from_id).first()
            role: Role = user.user_role
            return getattr(role, self.require)

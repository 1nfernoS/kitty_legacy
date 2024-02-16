from collections.abc import Sequence

from vkbottle.dispatch.rules import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from data_typings.enums import RoleAccess


class WhiteListChatRule(ABCRule[BaseMessageMin]):
    """
    Rule to check from where comes message.
    True if user not in ignore_users and chat in allowed_chats
    """
    def __init__(self, allowed_chats: Sequence[int]):
        self.allowed_chats = allowed_chats
        return

    async def check(self, event: BaseMessageMin) -> bool:
        return event.peer_id - 2e9 in self.allowed_chats


class AccessRule(ABCRule[BaseMessageMin]):
    """
    Rule to check access type for user's role
    return Role access
    """
    def __init__(self, require_access: RoleAccess):
        self.require = require_access.value
        return
    
    async def check(self, event: BaseMessageMin) -> bool:
        if event.from_id < 0:
            return False
        from ORM import session, User, Role
        with session() as s:
            user: User | None = s.query(User).filter(User.user_id == event.from_id).first()
            role: Role = user.user_role
            return getattr(role, self.require)


class FwdOrReplyUserRule(ABCRule[BaseMessageMin]):
    """
    Rule to check if message has Forward or Reply from user
    """
    async def check(self, event: BaseMessageMin) -> bool:
        if event.reply_message:
            return event.reply_message.from_id > 0
        if event.fwd_messages:
            return event.fwd_messages[0].from_id > 0
        return False

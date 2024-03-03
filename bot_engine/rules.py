from collections.abc import Sequence

from vkbottle.dispatch.rules import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from data_typings.enums import RoleAccess

from config import PIT_BOT


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
            result = getattr(role, self.require)
        if self.require == RoleAccess.profile_app:
            message = "Сдайте ссылку на профиль мне в лс!\n" \
                      "Проще всего это сделать через сайт, скопировав адрес ссылки кнопки 'Профиль' в приложении.\n" \
                      "Если получилась ссылка формата 'https:// vip3.activeusers .ru/блаблабла', то все получится)"
            await event.answer(message)
        return result


class FwdOrReplyUserRule(ABCRule[BaseMessageMin]):
    """
    Rule to check if message has Forward or Reply from user
    """
    
    def __init__(self, allow_self: bool = True):
        self.allow_self = allow_self
        return
    
    async def check(self, event: BaseMessageMin) -> bool:
        if event.reply_message:
            check_self = event.reply_message.from_id == event.from_id if not self.allow_self else True
            return event.reply_message.from_id > 0 and check_self
        if event.fwd_messages:
            check_self = event.fwd_messages[0].from_id == event.from_id if not self.allow_self else True
            return event.fwd_messages[0].from_id > 0 and check_self
        return False


class FwdPitRule(ABCRule[BaseMessageMin]):
    """
    Rule to check if message is Forwarded from pit
    """
    
    def __init__(self, only_first: bool = True):
        self.only_first = only_first
        return
    
    async def check(self, event: BaseMessageMin) -> bool:
        if event.fwd_messages:
            return (event.fwd_messages[0].from_id == PIT_BOT and
                    len(event.fwd_messages) == 1) if self.only_first else True
        return False


class FwdPitRule(ABCRule[BaseMessageMin]):
    """
    Rule to check if message is Forwarded from pit
    """
    
    def __init__(self, only_first: bool = True):
        self.only_first = only_first
        return
    
    async def check(self, event: BaseMessageMin) -> bool:
        if event.fwd_messages:
            return (event.fwd_messages[0].from_id == PIT_BOT and
                    len(event.fwd_messages) == 1) if self.only_first else True
        return False

from collections.abc import Sequence
from typing import Iterable

import vbml

from vkbottle.dispatch.rules import ABCRule
from vkbottle.tools.dev.mini_types.bot import MessageEventMin, MessageMin

from data_typings.enums import EventPayloadAction, RoleAccess

from config import PIT_BOT, OVERSEER_BOT
from utils.formatters import translate


class WhiteListChatRule(ABCRule[MessageMin]):
    """
    Rule to check from where comes message.
    True if user not in ignore_users and chat in allowed_chats
    """
    
    def __init__(self, allowed_chats: Sequence[int]):
        self.allowed_chats = allowed_chats
        return
    
    async def check(self, event: MessageMin) -> bool:
        return event.peer_id - 2e9 in self.allowed_chats


class AccessRule(ABCRule[MessageMin]):
    """
    Rule to check access type for user's role
    return Role access
    """
    
    def __init__(self, require_access: RoleAccess):
        self.require = require_access.value
        return
    
    async def check(self, event: MessageMin) -> bool:
        if event.from_id < 0:
            return False
        from ORM import session, User, Role
        with session() as s:
            user: User | None = s.query(User).filter(User.user_id == event.from_id).first()
            role: Role = user.user_role
            # noinspection PyTypeChecker
            result = getattr(role, self.require)
        return result


class HelpGroup(ABCRule[MessageMin]):
    """
    Dummy rule for `help` descriptions
    Must be in all bot message labelers
    """
    def __init__(self, cmd_group: str):
        self.cmd_group = cmd_group
        return

    async def check(self, event: MessageMin) -> bool:
        return True


class OverseerRule(ABCRule[MessageMin]):
    """
    Rule to check if message sent by overseer bot
    """
    def __init__(self, pattern: str | vbml.Pattern | Iterable[str] | Iterable[vbml.Pattern]):
        if isinstance(pattern, str):
            pattern = [vbml.Pattern(pattern)]
        elif isinstance(pattern, vbml.Pattern):
            pattern = [pattern]
        elif isinstance(pattern, Iterable):
            pattern = [
                p if isinstance(p, vbml.Pattern) else vbml.Pattern(p) for p in pattern
            ]
        self.patterns = pattern
        self.patcher = vbml.Patcher()
        return

    async def check(self, event: MessageMin) -> dict | bool:
        if event.from_id != OVERSEER_BOT:
            return False
        text = event.text.encode('cp1251', 'xmlcharrefreplace').decode('cp1251')
        for pattern in self.patterns:
            result = self.patcher.check(pattern, text)
            if result not in (None, False):
                return result
        return False


class FwdOrReplyUserRule(ABCRule[MessageMin]):
    """
    Rule to check if message has Forward or Reply from user
    """
    
    def __init__(self, allow_self: bool = True):
        self.allow_self = allow_self
        return
    
    async def check(self, event: MessageMin) -> bool:
        if event.reply_message:
            check_self = event.reply_message.from_id == event.from_id if not self.allow_self else True
            return event.reply_message.from_id > 0 and check_self
        if event.fwd_messages:
            check_self = event.fwd_messages[0].from_id == event.from_id if not self.allow_self else True
            return event.fwd_messages[0].from_id > 0 and check_self
        return False


class FwdPitRule(ABCRule[MessageMin]):
    """
    Rule to check if message is Forwarded from pit and contains certain text
    """
    
    def __init__(self, pattern: str | vbml.Pattern | Iterable[str] | Iterable[vbml.Pattern],
                 only_first: bool = True):
        if isinstance(pattern, str):
            pattern = [vbml.Pattern(pattern)]
        elif isinstance(pattern, vbml.Pattern):
            pattern = [pattern]
        elif isinstance(pattern, Iterable):
            pattern = [
                p if isinstance(p, vbml.Pattern) else vbml.Pattern(p) for p in pattern
            ]
        self.patterns = pattern
        self.patcher = vbml.Patcher()
        self.only_first = only_first
        return
    
    async def check(self, event: MessageMin) -> dict | bool:
        if not event.fwd_messages or event.fwd_messages[0].from_id != PIT_BOT:
            return False
        if self.only_first and len(event.fwd_messages) != 1:
            return False
        fwd_text = event.fwd_messages[0].text.encode('cp1251', 'xmlcharrefreplace').decode('cp1251')
        for pattern in self.patterns:
            result = self.patcher.check(pattern, fwd_text)
            if result not in (None, False):
                return {k: translate(result[k]) for k in result}
        return False


class ActionEventRule(ABCRule[MessageEventMin]):
    """
    Rule to check event matches action
    """
    
    def __init__(self, action_type: EventPayloadAction):
        self.action_type = action_type
        return
    
    async def check(self, event: MessageEventMin) -> bool:
        if not event.payload:
            return False
        if 'action' not in event.payload:
            return False
        return event.payload['action'] == self.action_type

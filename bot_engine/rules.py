from collections.abc import Sequence

from vkbottle.dispatch.rules import ABCRule
from vkbottle.tools.dev.mini_types.base import BaseMessageMin


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

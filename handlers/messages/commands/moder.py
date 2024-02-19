from typing import List

from vkbottle.tools.dev.mini_types.bot import MessageMin

from bot_engine import labeler
from bot_engine.rules import AccessRule, FwdOrReplyUserRule

from ORM import session, User, Role

from data_typings.enums import RoleAccess


@labeler.message(FwdOrReplyUserRule(), AccessRule(RoleAccess.change_role), text=['role <name>', 'роль <name>'])
async def change_role(msg: MessageMin, name: str):
    with session() as s:
        roles: List[Role] = s.query(Role).all()
    if name not in [r.alias for r in roles] and name not in [r.name for r in roles]:
        await msg.answer(f'Роль {name} не существует, проверьте написание или обратитесь к создателю')


from vkbottle.tools.dev.mini_types.bot import MessageMin

from bot_engine import labeler
from bot_engine.rules import AccessRule

from ORM import session, User, Role

from data_typings.enums import RoleAccess


@labeler.message(AccessRule(RoleAccess.bot_access), text=['ping', 'пинг'])
async def ping(msg: MessageMin):
    await msg.answer('ya jivoy xd')

from vkbottle.tools.dev.mini_types.bot import MessageMin

from bot_engine import labeler
from bot_engine.rules import AccessRule

from ORM import session, User, Role

from data_typings.enums import RoleAccess


@labeler.message(AccessRule(RoleAccess.bot_access), text=['ping', 'пинг'])
async def ping(msg: MessageMin):
    await msg.answer('ya jivoy xd')

@labeler.message(AccessRule(RoleAccess.bot_access), text=['role', 'роль'])
async def role(msg: MessageMin):
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == msg.from_id).first()
        if not user:
            s.add(User(user_id=msg.from_id))
            s.commit()
            user: User | None = s.query(User).filter(User.user_id == msg.from_id).first()
        user_role: Role = user.user_role
    await msg.answer(f'Ваша роль - {user_role.alias.capitalize()}')


from typing import List

from sqlalchemy import or_
from vkbottle.tools.dev.mini_types.bot import MessageMin

from bot_engine import labeler
from bot_engine.rules import AccessRule, FwdOrReplyUserRule

from ORM import session, Role, User

from data_typings.enums import RoleAccess, Roles


@labeler.message(FwdOrReplyUserRule(), AccessRule(RoleAccess.change_role), text=['role <name>', 'роль <name>'])
async def change_role(msg: MessageMin, name: str):
    name = name.lower()
    target_id: int = msg.reply_message.from_id if msg.reply_message else msg.fwd_messages[0].from_id
    with session() as s:
        roles: List[Role] = s.query(Role).all()
        user_role: Role | None = s.query(Role).filter(Role.role_users.any(User.user_id == msg.from_id)).first()
        target_role: Role | None = s.query(Role).filter(Role.role_users.any(User.user_id == target_id)).first()
    if name not in [r.alias for r in roles] and name not in [r.name for r in roles]:
        return await msg.answer(f'Роль {name} не существует, проверьте написание или обратитесь к создателю')

    if getattr(Roles, user_role.name) >= getattr(Roles, target_role.name):
        return await msg.answer(f'Ваша роль {user_role.alias} ниже или равна '
                                f'изменяемой роли {target_role.alias}, изменение невозможно')
    with session() as s:
        target_user: User | None = s.query(User).filter(User.user_id == target_id).first()
        new_role: Role | None = s.query(Role).filter(or_(Role.name == name, Role.alias == name)).first()
        target_user.role_name = new_role.name
        s.add(target_user)
        s.commit()

        return await msg.answer(f"Теперь пользователь имеет права {new_role.alias.capitalize()}")

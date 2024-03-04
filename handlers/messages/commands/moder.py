from typing import List, Literal

from sqlalchemy import or_
from vkbottle.tools.dev.mini_types.bot import MessageMin

from bot_engine import labeler, api
from bot_engine.rules import AccessRule, FwdOrReplyUserRule

from ORM import session, Role, User

from data_typings.enums import RoleAccess, Roles, guild_roles
from data_typings.emoji import gold


@labeler.message(FwdOrReplyUserRule(), AccessRule(RoleAccess.change_role), text=['role <name:str>', 'роль <name:str>'])
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


@labeler.message(FwdOrReplyUserRule(), AccessRule(RoleAccess.moderator), text=['kick', 'кик'])
async def ban_user(msg: MessageMin):
    target_id: int = msg.reply_message.from_id if msg.reply_message else msg.fwd_messages[0].from_id
    if target_id == msg.from_id:
        return await msg.answer(f"Нельзя кикнуть самого себя!")

    with session() as s:
        user_role: Role | None = s.query(Role).filter(Role.role_users.any(User.user_id == msg.from_id)).first()
        target_role: Role | None = s.query(Role).filter(Role.role_users.any(User.user_id == target_id)).first()
        if getattr(Roles, user_role.name) >= getattr(Roles, target_role.name):
            return await msg.answer(f'Ваша роль {user_role.alias} ниже или равна '
                                    f'роли {target_role.alias}, нельзя исключить')
        target_user: User | None = s.query(User).filter(User.user_id == target_id).first()
        if target_user:
            new_role: Role | None = s.query(Role).filter(Role.name == Roles.blacklist.name).first()
            target_user.role_name = new_role.name
            s.add(target_user)
            s.commit()

    await api.messages.remove_chat_user(msg.chat_id, target_id)
    
    return await msg.answer(f"@id{target_id} успешно кикнут!")


def _change_balance(target_id: int, value: int, action: Literal['change', 'set']) -> str:
    try:
        value = int(value)
    except ValueError:
        return 'Это не число (можно использовать + или - и число'

    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == target_id).first()
        if not user:
            return 'Этого игрока нет в моих записях, пусть напишет что-нибудь'
        if not user.user_role.balance_access:
            return 'У игрока нет баланса, пусть вступит гильдию или получит другую роль'
        if action == 'change':
            user.balance += value
        elif action == 'set':
            user.balance = value
        balance = user.balance
        s.add(user)
        s.commit()

    return f"Готово, изменил баланс на {value}{gold}\nНа счету игрока: {balance}{gold}"


@labeler.message(FwdOrReplyUserRule(), AccessRule(RoleAccess.change_balance),
                 text=['чек = <value>', 'check = <value>'])
async def set_balance(msg: MessageMin, value: int):
    target_id: int = msg.reply_message.from_id if msg.reply_message else msg.fwd_messages[0].from_id
    answer = _change_balance(target_id, value, 'set')
    return await msg.answer(answer)


@labeler.message(FwdOrReplyUserRule(), AccessRule(RoleAccess.change_balance),
                 text=['чек <value>', 'check <value>'])
async def change_balance(msg: MessageMin, value: int):
    target_id: int = msg.reply_message.from_id if msg.reply_message else msg.fwd_messages[0].from_id
    answer = _change_balance(target_id, value, 'change')
    return await msg.answer(answer)


@labeler.message(AccessRule(RoleAccess.moderator),
                 text=['налоговая', 'bill'])
async def bill(msg: MessageMin):
    with session() as s:
        users: List[User] | None = s.query(User).filter(User.role_name.in_([i.name for i in guild_roles])).all()
        for user in users:
            user.balance -= user.stat_level * 140
            s.add(user)
        s.commit()
    return await msg.answer(f"Списал налог с баланса, проверять можно командой баланс")

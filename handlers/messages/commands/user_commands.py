from typing import List

from vkbottle.tools.dev.mini_types.bot import MessageMin
from vkbottle import Keyboard, KeyboardButtonColor, OpenLink

from bot_engine import labeler
from bot_engine.rules import AccessRule, FwdOrReplyUserRule

from ORM import session, User

from config import GUILD_NAME, NOTE_RULES, NOTE_ALL

from data_typings.enums import RoleAccess, Roles
from utils.math import commission_price


@labeler.message(FwdOrReplyUserRule(), AccessRule(RoleAccess.balance_access),
                 text=['баланс', 'счет', 'счёт', 'balance', 'wallet'])
async def other_balance(msg: MessageMin):
    target_id: int = msg.reply_message.from_id if msg.reply_message else msg.fwd_messages[0].from_id
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == target_id).first()

    message = f"Долг игрока: {-user.balance}(Положить {commission_price(-int(user.balance))})" \
        if user.balance < 0 \
        else f"На счету игрока: {user.balance}"
    return await msg.answer(message)


@labeler.message(AccessRule(RoleAccess.balance_access), text=['баланс', 'счет', 'счёт', 'balance', 'wallet'])
async def balance(msg: MessageMin):
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == msg.from_id).first()

    message = f"Ваш долг: {-user.balance}(Положить {commission_price(-int(user.balance))})" \
        if user.balance < 0 \
        else f"Сейчас на счету: {user.balance}"
    return await msg.answer(message)


@labeler.message(AccessRule(RoleAccess.change_balance),
                 text=['баланс все', 'счет все', 'счёт все', 'balance all', 'wallet all'])
async def all_balance(msg: MessageMin):
    guild_roles = (Roles.creator, Roles.leader, Roles.captain, Roles.officer, Roles.guild, Roles.newbie)
    with session() as s:
        users: List[User] | None = s.query(User).filter(User.role_name.in_([i.name for i in guild_roles])).all()
    if not users:
        return await msg.answer('Нет данных')
    message = f"Баланс участников гильдии {GUILD_NAME}:"
    for user in users:
        message += f"\n@id{user.user_id}: {user.balance}"
    return await msg.answer(message)


@labeler.message(AccessRule(RoleAccess.bot_access),
                 text=['заметки', 'rules', 'notes', 'правила'])
async def change_balance(msg: MessageMin):
    kbd = Keyboard(inline=True)
    kbd.add(OpenLink(NOTE_RULES, 'Правила'), KeyboardButtonColor.SECONDARY)
    kbd.add(OpenLink(NOTE_ALL, 'Все заметки'), KeyboardButtonColor.SECONDARY)
    return await msg.answer('Заметки:', keyboard=kbd.get_json())

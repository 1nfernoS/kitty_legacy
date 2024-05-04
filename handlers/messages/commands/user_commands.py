from typing import List

from vkbottle.tools.dev.mini_types.bot import MessageMin
from vkbottle import Keyboard, KeyboardButtonColor, OpenLink, VKAPIError

from bot_engine import labeler, api
from bot_engine.rules import AccessRule, FwdOrReplyUserRule

from ORM import session, User

from config import GUILD_NAME, NOTE_RULES, NOTE_ALL

from data_typings.enums import RoleAccess, guild_roles
from resources.emoji import gold
from utils.formatters import format_name
from utils.math import commission_price


@labeler.chat_message(FwdOrReplyUserRule(), AccessRule(RoleAccess.balance_access),
                      text=['баланс', 'счет', 'счёт', 'balance', 'wallet'])
async def other_balance(msg: MessageMin):
    target_id: int = msg.reply_message.from_id if msg.reply_message else msg.fwd_messages[0].from_id
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == target_id).first()

    message = f"Долг игрока: {-user.balance}(Положить {commission_price(-int(user.balance))})" \
        if user.balance < 0 \
        else f"На счету игрока: {user.balance}"
    return await msg.answer(message)


@labeler.chat_message(AccessRule(RoleAccess.balance_access), text=['баланс', 'счет', 'счёт', 'balance', 'wallet'])
async def balance(msg: MessageMin):
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == msg.from_id).first()

    message = f"Ваш долг: {-user.balance}{gold}(Положить {commission_price(-int(user.balance))})" \
        if user.balance < 0 \
        else f"Сейчас на счету: {user.balance}{gold}"
    return await msg.answer(message)


@labeler.chat_message(AccessRule(RoleAccess.change_balance),
                      text=['баланс все', 'счет все', 'счёт все', 'balance all', 'wallet all'])
async def all_balance(msg: MessageMin):
    with session() as s:
        # noinspection PyTypeChecker
        users: List[User] | None = s.query(User).filter(User.role_name.in_([i.name for i in guild_roles])).all()
    if not users:
        return await msg.answer('Нет данных')
    message = f"Баланс участников гильдии {GUILD_NAME}:"
    for user in users:
        message += f"\n{await format_name(user.user_id, 'nom')}: {user.balance}{gold}"
    try:
        await api.messages.send(msg.from_id, 0, message=message)
    except VKAPIError[902, 901]:
        return await msg.answer('Разрешите  мне писать вам сообщения или просто напишите мне что-нибудь')
    return await msg.answer('Отправил список в лс')


@labeler.chat_message(AccessRule(RoleAccess.bot_access),
                      text=['заметки', 'rules', 'notes', 'правила'])
async def notes(msg: MessageMin):
    kbd = Keyboard(inline=True)
    kbd.add(OpenLink(NOTE_RULES, 'Правила'), KeyboardButtonColor.SECONDARY)
    kbd.add(OpenLink(NOTE_ALL, 'Все заметки'), KeyboardButtonColor.SECONDARY)
    return await msg.answer('Заметки:', keyboard=kbd.get_json())


@labeler.chat_message(FwdOrReplyUserRule(), AccessRule(RoleAccess.balance_access),
                      text=['перевести <amount:int>', 'transfer <amount:int>'])
async def transfer_money(msg: MessageMin, amount: int):
    try:
        amount = int(amount)
    except ValueError:
        return await msg.answer('Я не могу перевести не число')

    if amount <= 0:
        return await msg.answer('Нельзя перевести 0 или меньше золота!')

    target_id: int = msg.reply_message.from_id if msg.reply_message else msg.fwd_messages[0].from_id
    if target_id == msg.from_id:
        return await msg.answer('Перевод самому себе, не стоит')

    with session() as s:
        # noinspection PyTypeChecker
        user_from: User = s.query(User).filter(User.user_id == msg.from_id).first()
        # noinspection PyTypeChecker
        user_to: User = s.query(User).filter(User.user_id == target_id).first()

        if not user_to:
            return await msg.answer('Нет записей об игроке, пусть напишет что-нибудь')
        if not user_to.user_role.balance_access:
            return await msg.answer(f'У игрока нет доступа к балансу(Роль{user_to.role_name}), нужна другая роль')
        if user_from.balance < amount:
            return await msg.answer(f'Недостаточно средств! (На счету {user_from.balance}{gold})')

        user_from.balance -= amount
        user_to.balance += amount
        s.add(user_from)
        s.add(user_to)
        s.commit()

        return await msg.answer(f'Перевел {amount}{gold}!\n На счету осталось {user_from.balance}{gold}')

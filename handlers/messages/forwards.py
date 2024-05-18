from typing import List, Literal, Dict

from datetime import datetime, timedelta

from sqlalchemy import func

from vkbottle import VKAPIError
from vkbottle.tools.dev.mini_types.bot import MessageMin

import profile_api
import utils
from ORM import Item, session, User, LogsElites, LogsSiege
from bot_engine import labeler, api
from bot_engine.rules import FwdPitRule
from config import DISCOUNT_PERCENT, creator_id
from data_typings.enums import guild_roles, SiegeRole
from resources import emoji, get_puzzles
from resources.items import symbols_answers
from utils.formatters import frequent_letter
from utils.datetime import now
from utils.parsers import cross_signs


@labeler.message(FwdPitRule(f'{emoji.item}1*<item_name>\n{emoji.gold}Цена: <item_price:int> золота'))
async def dark_vendor(msg: MessageMin, item_name: str, item_price: int):
    msg_to_edit = await msg.answer('Проверяю торговца...')
    with session() as s:
        item: Item | None = s.query(Item).filter(Item.name == item_name, Item.has_price == 1).first()
    if not item:
        return await api.messages.edit(msg_to_edit.peer_id, 'Кажется, такой предмет не продается на аукционе',
                                       conversation_message_id=msg_to_edit.conversation_message_id)
    auc_price = await profile_api.get_price(item.id)
    commission_price = utils.math.commission_price(item_price)
    if auc_price <= 0:
        msg = (f'Товар: {emoji.item}{item_name}'
               f'\nЦена торговца: {emoji.gold}{item_price} ({emoji.gold}{commission_price})'
               f'\nВот только... Он не продается, Сам не знаю почему')
    else:
        guild_price = utils.math.discount_price(auc_price)
        guild_commission_price = utils.math.commission_price(guild_price)
        msg = f'Товар: {emoji.item}{item_name}\nЦена торговца: {emoji.gold}{item_price} ' \
              f'({emoji.gold}{commission_price})' + \
              f'\nЦена аукциона: {emoji.gold}{auc_price} (со скидкой гильдии {DISCOUNT_PERCENT}%: ' \
              f'{emoji.gold}{guild_price}' \
              f'({emoji.gold}{guild_commission_price})\n\n'
    return await api.messages.edit(msg_to_edit.peer_id, msg,
                                   conversation_message_id=msg_to_edit.conversation_message_id)


@labeler.message(FwdPitRule(f'Символы:\n<regex>\nОтправьте букву или текст:'))
async def symbol_guesser(msg: MessageMin, regex: str):
    msg_to_edit = await msg.answer('Символы, сейчас...')
    with session() as s:
        # noinspection PyTypeChecker
        item_list: List[Item] = s.query(Item).filter(
            Item.name.op('regexp')(f"(Книга - |^){regex.replace(emoji.empty, '[[:alnum:]]')}$")).all()
    res = []
    for i in item_list:
        if i.id in symbols_answers or '-' in i.name:
            res.append(i.name.replace('Книга - ', ''))

    msg = 'Это наверняка что-то из этого:\n'

    if not regex.replace(emoji.empty, '').replace(' ', ''):
        best_guess = frequent_letter(res)
        msg = f'Попробуй букву {best_guess.upper()} ! ' + msg
    msg += '\n'.join(res)
    return await api.messages.edit(msg_to_edit.peer_id, msg,
                                   conversation_message_id=msg_to_edit.conversation_message_id)


@labeler.message(FwdPitRule(f'<text1>\n<text2>\n\n&#8987;Путешествие продолжается...\n<notice>'))
async def travel_check(msg: MessageMin, notice: str):
    res: Literal["safe", "warn", "danger"] | None = get_puzzles()['travel'].get(notice)
    if not res:
        return await msg.answer(f"(+?) Неизвестное событие, сообщите в полигон или [id{creator_id}|ему]")
    answer: Dict[Literal["safe", "warn", "danger"], str] = {
        'safe': f"(+1) Можно продолжать путешествие",
        'warn': f"(+2) Можно продолжать путешествие",
        'danger': f"(+3) Событие предшествует смертельному!"
    }

    res = await msg.reply(answer.get(res))

    try:
        await api.messages.delete(cmids=[msg.conversation_message_id], delete_for_all=True, peer_id=msg.peer_id)
    except VKAPIError[15]:  # message from admin
        pass
    return res


@labeler.message(FwdPitRule(['Дверь с грохотом открывается<text>\n\n<text1>', 'Дверь с грохотом открывается<text>']))
async def door_answer(msg: MessageMin, text: str):
    res: str | None = None
    puzzles = get_puzzles()
    for riddle in puzzles['door']:
        if riddle in text:
            res = puzzles['door'][riddle]

    if not res:
        return await msg.answer(f"Ой, а я не знаю ответ\nCообщите в полигон или [id{creator_id}|ему]")

    res = await msg.reply(f'Открываем дверь, а там ответ: {res}')

    try:
        await api.messages.delete(cmids=[msg.conversation_message_id], delete_for_all=True, peer_id=msg.peer_id)
    except VKAPIError[15]:  # message from admin
        pass
    return res


@labeler.message(FwdPitRule('Книгу целиком уже не спасти, но одна из страниц уцелела. Кусок текста на ней гласит: '
                            '«...<page_text>...».'
                            '\nОсталось определить, какая именно это была книга...'))
async def book_answer(msg: MessageMin, page_text: str):
    res: str | None = None
    puzzles = get_puzzles()
    for page in puzzles['pages']:
        if page in page_text:
            res = puzzles['pages'][page]

    if not res:
        return await msg.answer(f"Ой, а я не знаю ответ\nCообщите в полигон или [id{creator_id}|ему]")

    res = await msg.reply(f'Это страница из книги {res}')

    try:
        await api.messages.delete(cmids=[msg.conversation_message_id], delete_for_all=True, peer_id=msg.peer_id)
    except VKAPIError[15]:  # message from admin
        pass
    return res


@labeler.message(FwdPitRule('Вы успешно обменяли элитные трофеи (<count:int>) на репутацию гильдии!'
                            '\n&#127941;Текущая репутация гильдии: <all_count:int>'))
async def elite_answer(msg: MessageMin, count: int):
    date = datetime.utcfromtimestamp(msg.fwd_messages[0].date)
    today = now()
    first_day = today.replace(day=1)
    last_day = today.replace(month=today.month % 12 + 1, year=today.year + (today.month // 12)) - timedelta(days=1)
    with (session() as s):
        user: User | None = s.query(User).filter(User.user_id == msg.from_id).first()
        role = user.user_role
    if role.name not in [i.name for i in guild_roles]:
        return

    if date.date() != now().date():
        return await msg.answer('Мне нужны элитные трофеи сданные лишь сегодня')

    if user.stat_level < 100:
        limit = 40
    elif user.stat_level < 250:
        limit = 90
    else:
        limit = 120

    LogsElites(msg.from_id, count).make_log()

    with session() as s:
        elites_count: int = s.query(func.sum(LogsElites.count)).filter(
            LogsElites.timestamp.between(first_day, last_day),
            LogsElites.user_id == msg.from_id).scalar()
    answer = f"Добавил {count} к элитным трофеям! Сдано за месяц: {elites_count}\n"
    answer += f"Осталось сдать {limit - elites_count} штук" \
        if limit > elites_count \
        else f"Сданы все необходимые трофеи"
    return await msg.reply(answer)


@labeler.message(FwdPitRule(
    f'Перед каждым проходом другими искателями приключений нацарапаны различные надписи, которые, '
    f'видимо, могут помочь определить, куда ведет конкретная дорога.\n'
    '&#128681;Западный путь: "<west_1>" и "<west_2>"\n'
    '&#128681;Северный путь: "<north_1>" и "<north_2>"\n'
    '&#128681;Восточный путь: "<east_1>" и "<east_2>"\n\n'
    'Осталось выбрать, какому направлению последовать...'))
async def cross_answer(msg: MessageMin, west_1: str, west_2: str, north_1: str, north_2: str, east_1: str, east_2: str):
    west, north, east = (cross_signs(*i) for i in ([west_1, west_2], [north_1, north_2], [east_1, east_2]))
    answer = "Направления ведут к\n"
    answer += f"{emoji.flag} Запад - Это {west}\n"
    answer += f"{emoji.flag} Север - Это {north}\n"
    answer += f"{emoji.flag} Восток - Это {east}\n"

    res = await msg.reply(answer)

    try:
        await api.messages.delete(cmids=[msg.conversation_message_id], delete_for_all=True, peer_id=msg.peer_id)
    except VKAPIError[15]:  # message from admin
        pass
    return res


@labeler.message(FwdPitRule('&#9989;Вы успешно присоединились к осадному лагерю гильдии <guild>!\n'
                            '&#128100;Ваша роль: <siege_role> (+<count:int>&#<emoji:int>;)'))
async def siege_answer(msg: MessageMin, guild: str, siege_role: str, count: int):
    date = datetime.utcfromtimestamp(msg.fwd_messages[0].date)

    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == msg.from_id).first()
        role = user.user_role
    if role.name not in [i.name for i in guild_roles]:
        return

    if date.date() != now().date():
        return await msg.answer('Я не принимаю отчеты по осаде за другие дни')

    with session() as s:
        # noinspection PyTypeChecker
        siege: List[LogsSiege] | None = s.query(LogsSiege).filter(
            LogsSiege.timestamp.between(now().replace(hour=0, minute=0, second=0),
                                        now().replace(hour=23, minute=59, second=59),
                                        LogsSiege.user_id == msg.from_id)).all()
    if siege:
        return await msg.reply('Твое участие уже зарегистрировано!')

    LogsSiege(msg.from_id, guild, SiegeRole(siege_role).name, count).make_log()

    answer = f"Зарегистрировал твое участие в осаде за {guild} ({siege_role} +{count})"
    return await msg.reply(answer)

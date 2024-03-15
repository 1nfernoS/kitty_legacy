from typing import List, Literal, Dict

from vkbottle import VKAPIError
from vkbottle.tools.dev.mini_types.bot import MessageMin

import profile_api
import utils
from ORM import Item, session
from bot_engine import labeler, api
from bot_engine.rules import FwdPitRule
from config import DISCOUNT_PERCENT, creator_id
from resources import emoji, puzzles
from resources.items import symbols_answers
from utils.formatters import frequent_letter


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
    res: Literal["safe", "warn", "danger"] | None = puzzles['travel'].get(notice)
    if not res:
        return await msg.answer(f"(+?) Неизвестное событие, сообщите в полигон или [id{creator_id}|ему]")
    answer: Dict[Literal["safe", "warn", "danger"], str] = {
        'safe': f"(+1) Можно продолжать путешествие",
        'warn': f"(+2) Можно продолжать путешествие",
        'danger': f"(+3) Событие предшествует смертельному!"
    }
    msg_id = await api.messages.get_by_conversation_message_id(msg.peer_id, msg.conversation_message_id)
    try:
        await api.messages.delete(
            message_ids=msg_id.items[0].id,
            delete_for_all=True
        )
    except VKAPIError[15]:  # message from admin
        pass
    return await msg.reply(answer.get(res))

@labeler.message(FwdPitRule(['Дверь с грохотом открывается<text>\n\n<text1>', 'Дверь с грохотом открывается<text>']))
async def door_answer(msg: MessageMin, text: str):
    res: str | None = None
    for riddle in puzzles['door']:
        if riddle in text:
            res = puzzles['door'][riddle]
    if not res:
        return await msg.answer(f"Ой, а я не знаю ответ\nCообщите в полигон или [id{creator_id}|ему]")

    msg_id = await api.messages.get_by_conversation_message_id(msg.peer_id, msg.conversation_message_id)
    try:
        await api.messages.delete(
            message_ids=msg_id.items[0].id,
            delete_for_all=True
        )
    except VKAPIError[15]:  # message from admin
        pass
    return await msg.reply(f'Открываем дверь, а там ответ: {res}')

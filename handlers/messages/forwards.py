from typing import List

from vkbottle.tools.dev.mini_types.bot import MessageMin

import profile_api
import utils
from ORM import Item, session
from bot_engine import labeler, api
from bot_engine.rules import FwdPitRule
from config import DISCOUNT_PERCENT
from data_typings import emoji
from data_typings.items import symbols_answers
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

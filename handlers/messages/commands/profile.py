from typing import List, Tuple

from vkbottle.tools.dev.mini_types.bot import MessageMin
from vkbottle_types.objects import MessagesSendUserIdsResponseItem

import profile_api
from bot_engine import labeler, api
from bot_engine.rules import AccessRule

from ORM import session, Item
from config import DISCOUNT_PERCENT

from data_typings.enums import RoleAccess
from utils.math import commission_price, discount_price


async def _item_price_base(msg: MessageMin, item: str, count: int = 1) -> MessagesSendUserIdsResponseItem:
    if len(item) < 3:
        return await msg.answer('Добавьте пару букв к поиску, чтобы их было хотя бы 3')

    msg_to_edit = msg.answer('Ищу ценники . . .')

    with session() as s:
        search: List[Item] = s.query(Item).filter(
            Item.name.op('regexp')(f"(Книга - |Книга - [[:alnum:]]+ |^[[:alnum:]]+ |^){item}.*$"),
            Item.has_price == 1).all()

    answer = ''
    cnt = 0
    for i in search:
        auc_price = await profile_api.get_price(i.id)
        if auc_price <= 0:
            continue

        guild_price = discount_price(auc_price)
        guild_commission_price = commission_price(guild_price)
        answer += f"\n{auc_price if count == 1 else auc_price * count} "
        answer += f"[-{DISCOUNT_PERCENT}%:{guild_price if count == 1 else guild_price * count} "
        answer += f"({guild_commission_price if count == 1 else guild_commission_price * count})] "
        answer += f"{i.name}"
        cnt += 1

    answer = f"Нашел следующее:" + answer if cnt > 0 else 'Ничего не нашлось...'

    msg_to_edit = await msg_to_edit
    return await api.messages.edit(msg_to_edit.peer_id, answer,
                                   conversation_message_id=msg_to_edit.conversation_message_id)


@labeler.message(AccessRule(RoleAccess.bot_access), text=['цена <item> - <count>', 'price <item> - <count>'])
async def item_price_many(msg: MessageMin, item: str, count: int):
    try:
        count = int(count)
    except ValueError:
        return await msg.answer('Это не число')
    return await _item_price_base(msg, item, count)


@labeler.message(AccessRule(RoleAccess.bot_access), text=['цена <item>', 'price <item>'])
async def item_price(msg: MessageMin, item: str):
    return await _item_price_base(msg, item)



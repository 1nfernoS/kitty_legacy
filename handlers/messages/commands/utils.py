from typing import List
from data_typings.enums import RoleAccess

from vkbottle.tools.dev.mini_types.bot import MessageMin

from bot_engine import labeler
from bot_engine.rules import AccessRule, FwdOrReplyUserRule

from ORM import session, User, Role

from utils.math import pure_price, commission_price


@labeler.chat_message(AccessRule(RoleAccess.bot_access), text=['ping', 'пинг'])
async def ping(msg: MessageMin):
    from random import choice
    answers: List[str] = ["Я живой", "Да живой я", "Все в порядке", "понг", "Что-то случилось?", "Не стучи ><",
                          "Внимание, анекдот", "Очередной текст на выбор", "Здесь могла быть ваша реклама",
                          "Кстати, можете мне в ЛС предложить идею!", "Мой профиль", "Утро доброе", "Я не сплю",
                          "Добрый день", "Добрый вечер", "Провел проверки, все работает", "Мяу", "Мяу :3", ":3",
                          "М-р-р-р-р"]
    await msg.answer(choice(answers))


@labeler.chat_message(AccessRule(RoleAccess.bot_access), text=['грязными <money:int>', 'dirty <money:int>'])
async def dirty(msg: MessageMin, money: int):
    try:
        await msg.answer(pure_price(int(money)))
    except ValueError:
        return


@labeler.chat_message(AccessRule(RoleAccess.bot_access), text=['чистыми <money:int>', 'pure <money:int>'])
async def pure(msg: MessageMin, money: int):
    try:
        await msg.answer(commission_price(int(money)))
    except ValueError:
        return


@labeler.chat_message(AccessRule(RoleAccess.admin_utils),
                      text=['обнови предметы <start:int> <end:int>',
                            'update items <start:int> <end:int>',
                            'обновить предметы <start:int> <end:int>'])
async def update_items(msg: MessageMin, start: int, end: int):
    try:
        start = int(start)
        end = int(end)
    except ValueError:
        return
    return await msg.answer('Не прописан парсер колодца, работаем над этим...')

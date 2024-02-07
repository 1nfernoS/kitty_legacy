from typing import List

from vkbottle.tools.dev.mini_types.bot import MessageMin

from bot_engine import labeler
from bot_engine.rules import AccessRule

from ORM import session, User, Role

from data_typings.enums import RoleAccess
from utils.math import pure_price, commission_price


@labeler.message(AccessRule(RoleAccess.bot_access), text=['ping', 'пинг'])
async def ping(msg: MessageMin):
    from random import choice
    answers: List[str] = ["Я живой", "Да живой я", "Все в порядке", "понг", "Что-то случилось?", "Не стучи ><",
                          "Внимание, анекдот", "Очередной текст на выбор", "Здесь могла быть ваша реклама",
                          "Кстати, можете мне в ЛС предложить идею!", "Мой профиль", "Утро доброе", "Я не сплю",
                          "Добрый день", "Добрый вечер", "Провел проверки, все работает", "Мяу", "Мяу :3", ":3",
                          "М-р-р-р-р"]
    await msg.answer(choice(answers))


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


@labeler.message(AccessRule(RoleAccess.bot_access), text=['грязными <money>', 'dirty <money>'])
async def dirty(msg: MessageMin, money: int):
    try:
        await msg.answer(pure_price(int(money)))
    except ValueError:
        return


@labeler.message(AccessRule(RoleAccess.bot_access), text=['чистыми <money>', 'pure <money>'])
async def pure(msg: MessageMin, money: int):
    try:
        await msg.answer(commission_price(int(money)))
    except ValueError:
        return
        

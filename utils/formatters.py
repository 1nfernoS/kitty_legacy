from datetime import datetime
from typing import Literal, List

from data_typings.profile import Skills
from resources.emoji import tab, active_book, passive_book, gold
from .math import commission_price


def format_profile_skills(item_list: list, skills: Skills) -> str:
    from ORM import session, Item
    message = ''
    with session() as s:
        for book in item_list:
            b_item: Item = s.query(Item).filter(Item.id == book).first()

            lvl = None
            if "(А) " in b_item.name:
                book_name = b_item.name.replace("(А) ", f"{tab}{active_book}")
                lvl = [skill['level'] for skill in skills['active'] if b_item.name[4:].startswith(skill['name'][:-1])]

            if "(П) " in b_item.name:
                book_name = b_item.name.replace("(П) ", f"{tab}{passive_book}")
                lvl = [skill['level'] for skill in skills['passive'] if b_item.name[4:].startswith(skill['name'][:-1])]
            message += '\n' + f'{book_name}'
            if lvl:
                message += f" - {lvl[0]} ({(round((int(lvl[0]) / 10) ** 0.5 * 10) + 100)}%)"
    return message


async def format_name(user_id: int, case: Literal["nom", "gen", "dat", "acc", "ins", "abl"] = 'gen') -> str:
    from bot_engine import api
    user = await api.users.get(user_id, name_case=case)
    return f"[id{user[0].id}|{user[0].first_name}]"


def frequent_letter(word_list: List[str]) -> str:
    letters = []
    if len(word_list) == 1:
        letters += list(word_list[0])
    else:
        for word in word_list:
            letters += list(set(word))
    return max(letters, key=lambda x: letters.count(x))

def translate(text: str) -> str:
    if not isinstance(text, str):
        return text
    translate_dict = {'A': 'А', 'B': 'В', 'C': 'С', 'E': 'Е', 'H': 'Н', 'K': 'К', 'M': 'М', 'O': 'О', 'P': 'Р',
                      'T': 'Т', 'X': 'Х', 'a': 'а', 'c': 'с', 'e': 'е', 'o': 'о', 'p': 'р', 'x': 'х', 'y': 'у'}
    for letter in translate_dict:
        text = text.replace(letter, translate_dict[letter])
    return text


def balance_message_addition(balance: int) -> str:
    return f"Ваш долг: {gold}{-int(balance)}(Положить {commission_price(-int(balance))} золота)" \
        if balance < 0 else f"Сейчас на счету: {gold}{balance}"

def date_diff(d1: datetime, d2: datetime) -> str:
    diff = max(d1, d2) - min(d1, d2)
    res = 'Прошло '
    if diff.days:
        res += str(diff.days)
        if diff.days // 10 == 1 or diff.days % 10 > 4:
            res += ' дней '
        elif diff.days // 10 > 1 and diff.days % 10 == 0:
            res += ' дней '
        elif diff.days % 10 > 1:
            res += ' дня '
        elif diff.days % 10 == 1:
            res += ' день '
    h = diff.seconds // 3600
    if h:
        res += str(h)
        if h // 10 == 1 or h % 10 > 4 or h % 10 == 0:
            res += ' часов '
        elif h % 10 > 1:
            res += ' часа '
        elif h % 10 == 1:
            res += ' час '
    # even if d1==d2, result will be not empty
    m = diff.seconds % 3600 // 60
    res += str(m)
    if m // 10 == 1 or m % 10 > 4 or m % 10 == 0:
        res += ' минут '
    elif m % 10 > 1:
        res += ' минуты '
    elif m % 10 == 1:
        res += ' минута '
    return res.strip() + f" c {min(d1, d2).strftime('%d.%m.%y %H:%M')}"

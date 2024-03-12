from typing import Literal, List

from data_typings.profile import Skills
from data_typings.emoji import tab, active_book, passive_book


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

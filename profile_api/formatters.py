from typing import List

from data_typings.profile import Build
from resources.items import (equipped_books_passive, equipped_books_active, adm_to_equipped_books,
                             equipped_to_ordinary_active, equipped_to_ordinary_passive, adm_to_ordinary_books)


def get_build(item_list: List[int]) -> Build:
    __BOOK_LIST = equipped_books_active + equipped_books_passive

    res: Build = {'books': [], 'adms': []}
    for item in item_list:
        if item in __BOOK_LIST:
            res['books'].append(item)
        if item in adm_to_equipped_books.keys():
            res['adms'] += adm_to_equipped_books[item]
    return res


def get_books(item_list: List[int]) -> List[int]:
    __BOOK_LIST = equipped_to_ordinary_active.copy()
    __BOOK_LIST.update(equipped_to_ordinary_passive.copy())
    __ADM_DICT = adm_to_ordinary_books.copy()
    res = []
    for item in item_list:
        if item in __BOOK_LIST.keys():
            res.append(__BOOK_LIST[item])
        if item in __ADM_DICT.keys():
            res += __ADM_DICT[item]
    return res

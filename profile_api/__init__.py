import json

import requests

from bs4 import BeautifulSoup

from config import PROFILE_KEY, PROFILE_ID


__url = 'http://vip3.activeusers.ru/app.php'
__params = {
    'group_id': 182985865,
    'api_id': 7055214,
    'auth_key': PROFILE_KEY,
    'viewer_id': PROFILE_ID,
    'act': 'user'
}


def _get_soup(**params) -> BeautifulSoup:
    __params.update(params)
    soup = BeautifulSoup(requests.get(__url, __params).content, 'html.parser')
    __params.update({'auth_key': PROFILE_KEY, 'viewer_id': PROFILE_ID})
    return soup


def get_name(item_id: int) -> str:
    soup = _get_soup(act='item', id=item_id)
    try:
        return soup.find_all('div', class_='shop_res-title')[0].contents[0].strip()
    except:
        return ''


def get_price(item_id: int) -> int:

    soup = _get_soup(act='item', id=item_id)

    try:
        t1 = soup.body
        try:
            t2 = t1.find_all('div', class_='portlet')[1]
            t3 = t2.find_all('script')[1]
            t4 = str(t3)[str(t3).find('window.graph_data'):]
            t5 = json.loads(t4[20:t4.find(';')])
            return round(sum([i[1] for i in t5]) / len(t5))
        except IndexError:
            return -1
    except TypeError:
        return -1

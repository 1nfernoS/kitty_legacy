import json

import aiohttp

from bs4 import BeautifulSoup

from config import PROFILE_KEY, PROFILE_ID


__url = 'https://vip3.activeusers.ru/app.php'
__params = {
    'group_id': 182985865,
    'api_id': 7055214,
    'auth_key': PROFILE_KEY,
    'viewer_id': PROFILE_ID,
    'act': 'user'
}


async def _get_soup(**params) -> BeautifulSoup:
    __params.update(params)
    async with aiohttp.ClientSession() as session:
        async with session.get(__url, params=__params) as response:
            result = await response.content.read()
    soup = BeautifulSoup(result, 'html.parser')
    __params.update({'auth_key': PROFILE_KEY, 'viewer_id': PROFILE_ID})
    return soup


async def get_name(item_id: int) -> str:
    soup = await _get_soup(act='item', id=item_id)
    try:
        return soup.find_all('div', class_='shop_res-title')[0].contents[0].strip()
    except:
        return ''


async def get_price(item_id: int) -> int:

    soup = await _get_soup(act='item', id=item_id)

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

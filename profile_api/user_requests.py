from typing import List

from . import _get_soup

from data_typings.profile import Skill, Skills, Stats, Profile
from resources.items import buff_classes, races


async def lvl_skills(auth_key: str, user_id: int) -> Skills:
    import re

    soup = await _get_soup(act='pages', id=702, auth_key=auth_key, viewer_id=user_id)

    a = soup.body.find_all('div', {'class': 'element-box'})[0]
    active, passive = a.find_all('p')
    p_level: List[Skill] = [{
        'name': i.split(':')[0],
        'level': int(re.findall(r'\d+', i.split(':')[1])[0])}
        for i in passive.get_text().split('\n')]
    a_level = [{
        'name': i.split(':')[0],
        'level': int(re.findall(r'\d+', i.split(':')[1])[0])}
        for i in active.get_text().split('\n')]
    return {'active': a_level, 'passive': p_level}


async def _stats(auth_key: str, user_id: int) -> Stats:
    soup = await _get_soup(act='user', auth_key=auth_key, viewer_id=user_id)

    stat = []
    for i in soup.body.find_all('span', class_='money-list-rescount'):
        stat.append(int(i.text.replace(u'\xa0', '')))
    res: Stats = {'level': stat[0], 'attack': stat[1], 'defence': stat[2],
                  'strength': stat[3], 'agility': stat[4], 'endurance': stat[5],
                  'luck': stat[6], 'accuracy': stat[7], 'concentration': stat[8]}
    return res


async def _inv(auth_key: str, user_id: int) -> List[int]:
    soup = await _get_soup(act='user', auth_key=auth_key, viewer_id=user_id)

    t1 = soup.body.find_all('div', class_='resitems items clearfix')[2]

    return [int(i['class'][1][1:]) for i in t1.find_all('a')]


async def get_profile(auth: str, id_vk: int) -> Profile:
    return {'items': await _inv(auth, id_vk), 'stats': await _stats(auth, id_vk)}


async def get_buff_class(auth_key: str, user_id: int) -> int | None:
    for val in await _inv(auth_key, user_id):
        if val in buff_classes:
            return val
    return None


async def get_player_races(auth_key: str, user_id: int) -> List[int]:
    return [val for val in await _inv(auth_key, user_id) if val in races]


async def get_buffer_voices(auth_key: str, user_id: int, class_id: int = 14264) -> int:
    soup = await _get_soup(act='item', auth_key=auth_key, viewer_id=user_id, id=class_id)

    voices = soup.find_all('h4')[0].text
    import re
    return int(re.findall(r'\d+(?=/\d+)', voices)[0])

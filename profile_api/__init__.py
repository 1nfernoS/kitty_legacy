import json

import aiohttp

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

data = {
    'Впереди все спокойно.': 'safe', 'Впереди не видно никаких препятствий.': 'safe',
    'Время пересечь мост через реку.': 'safe',
    'Вы бодры как никогда.': 'safe',
    'Густые деревья шумят на ветру.': 'safe',
    'Густые заросли травы по правую руку.': 'safe',
    'Дорога ведет прямиком к приключениям.': 'safe',
    'Дорога проходит мимо озера.': 'safe',
    'Идти легко, как никогда.': 'safe',
    'На небе ни единого облачка.': 'safe',
    'Не время останавливаться!': 'safe',
    'Ничего не предвещает беды.': 'safe',
    'Нужно двигаться дальше.': 'safe',
    'От широкой дороги ветвится небольшая тропинка.': 'safe',
    'Пение птиц доносится из соседнего леса.': 'safe',
    'Погода просто отличная.': 'safe',
    'Самое время найти еще что-то интересное.': 'safe',
    'Солнечная поляна виднеется впереди.': 'safe',
    'Стрекот сверчков заглушает другие звуки.': 'safe',
    'Только вперед!': 'safe',
    'Тропа ведет в густой лес.': 'safe',
    'Вас клонит в сон от усталости...': 'warn',
    'Возможно, стоит повернуть назад?..': 'warn',
    'Вдалеке слышны страшные крики...': 'warn',
    'Местность становится все опаснее и опаснее...': 'warn',
    'Нужно быть предельно осторожным...': 'warn',
    'Нужно ли продолжать путь...': 'warn',
    'Опасность может таиться за каждым деревом...': 'warn',
    'Путь становится все труднее...': 'warn',
    'С каждым шагом чувство тревоги нарастает...': 'warn',
    'Становится сложно разглядеть дорогу впереди...': 'warn',
    'Сердце громко стучит в груди...': 'warn',
    'Туман начинает сгущаться...': 'warn',
    'Тучи сгущаются над дорогой...': 'warn',
    'Боль разрывает Вас на части...': 'danger',
    'В воздухе витает отчетливый запах смерти...': 'danger',
    'Воздух просто гудит от опасности...': 'danger',
    'Вы уже на пределе...': 'danger',
    'Еще немного, и Вы падаете без сил...': 'danger',
    'Кажется, конец близок...': 'danger',
    'Крик отчаяния вырывается у Вас из груди...': 'danger',
    'Ноги дрожат от предчувствия беды...': 'danger',
    'Нужно бежать отсюда!': 'danger',
    'Силы быстро Вас покидают...': 'danger',
    'Смерть таится за каждым поворотом...': 'danger',
    'Чувство тревоги бьет в колокол!': 'danger',
    'Еще немного, и Вы падете без сил...': 'danger'
}
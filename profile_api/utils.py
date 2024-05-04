from typing import List, Dict

from . import _get_soup


async def sellable_items() -> List[int]:
    soup = await _get_soup(act='user')
    t1 = soup.find_all('li', class_='dropdown-submenu')
    sellable = [t1[1], t1[2], t1[3], t1[4], t1[5], t1[7], t1[8], t1[9], t1[10]]
    res = []
    for t in sellable:
        for i in t.find_all('li'):
            if i.span.text.startswith(' +'):
                data = i.a['href']
                res.append(int(data[data.find('&id=') + 4:data.find('&auth_key=')]))
    return res


async def ingredients() -> List[int]:
    soup = await _get_soup(act='user')
    t1 = soup.find_all('li', class_='dropdown-submenu')
    sellable = [t1[0]]
    res = []
    for t in sellable:
        for i in t.find_all('li'):
            data = i.a['href']
            res.append(int(data[data.find('&id=') + 4:data.find('&auth_key=')]))
    return res


async def header(param: int = 0) -> Dict[int, str]:
    soup = await _get_soup(act='user')
    t1 = soup.find_all('li', class_='dropdown-submenu')
    if 0 <= param < 17 and param != 13:
        sellable = [t1[param]]
    else:
        sellable = [*t1[:13], *t1[14:17]]

    res = {}
    for t in sellable:
        for i in t.find_all('li'):
            data = i.a['href']
            if 'act=item' in data:
                res[int(data[data.find('&id=') + 4:data.find('&auth_key=')])] = i.span.text.strip()
    return res

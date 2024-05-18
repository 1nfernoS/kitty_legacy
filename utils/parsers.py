from resources import get_puzzles


def cross_signs(arg1: str, arg2: str) -> str:
    puzzles = get_puzzles()
    data1 = puzzles['cross'].get(arg1.lower(), 'Неизвестно').split(',')
    data2 = puzzles['cross'].get(arg2.lower(), 'Неизвестно').split(',')
    res = []
    for a in data1:
        if a in data2:
            res.append(a)
    return ', '.join(res) if res else ', '.join(set(data1 + data2))

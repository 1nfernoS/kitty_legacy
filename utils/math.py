from config import DISCOUNT_PERCENT, GOLD_COMMISSION_PERCENT


def multiplier_percent(percent: int) -> float:
    return 100/(100-percent)


def commission_price(money: int, percentage: int = GOLD_COMMISSION_PERCENT) -> int:
    res = money * multiplier_percent(percentage)
    return round(res) if round(res) == res else int(res)+1


def pure_price(money: int, percentage: int = GOLD_COMMISSION_PERCENT) -> int:
    res = money / multiplier_percent(percentage)
    return round(res) if round(res) == res else int(res)


def discount_price(money: int) -> int:
    res = round(money / multiplier_percent(DISCOUNT_PERCENT))
    return round(res) if round(res) == res else int(res)+1

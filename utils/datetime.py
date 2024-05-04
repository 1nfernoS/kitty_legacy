import datetime as dt

from config import TZ

__all__ = ('now',)


def now() -> dt.datetime:
    return dt.datetime.utcnow() + dt.timedelta(hours=TZ)

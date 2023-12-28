from enum import Enum, auto


class ItemAction(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    PUT = auto()
    TAKE = auto()

    GET = auto()
    GIVE = auto()

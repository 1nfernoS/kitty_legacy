from enum import Enum, auto


class RoleAccess(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()
    
    bot_access = auto()
    admin_utils = auto()
    moderator = auto()
    change_role = auto()
    change_balance = auto()
    balance_access = auto()
    profile_app = auto()
    wallet = auto()
    take_money = auto()
    take_books = auto()
    take_ingredients = auto()
    take_buffs = auto()
    stats_access = auto()


class ItemAction(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    PUT = auto()
    TAKE = auto()

    GET = auto()
    GIVE = auto()

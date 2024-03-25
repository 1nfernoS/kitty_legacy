from enum import Enum, auto, IntEnum


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

    GIVE = auto()


class ChangeMoneyAction(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()

    ADD = auto()
    SUB = auto()
    SET = auto()


class SiegeRole(Enum):

    MAGE = 'маг'
    WARRIOR = 'боец'
    ARCHER = 'лучник'


class Roles(IntEnum):
    creator = 0
    leader = 1
    captain = 2
    officer = 3
    guild = 4
    newbie = 5
    guest = 6
    other = 7
    blacklist = 8


guild_roles = (Roles.creator, Roles.leader, Roles.captain, Roles.officer, Roles.guild, Roles.newbie)

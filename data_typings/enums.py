from enum import auto, IntEnum, StrEnum


class RoleAccess(StrEnum):
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


class ItemAction(StrEnum):
    PUT = auto()
    TAKE = auto()
    GIVE = auto()


class ChangeMoneyAction(StrEnum):
    ADD = auto()
    SUB = auto()
    SET = auto()


class SiegeRole(StrEnum):
    MAGE = 'маг'
    WARRIOR = 'боец'
    ARCHER = 'лучник'


class Roles(IntEnum):
    creator = 0
    leader = auto()
    captain = auto()
    officer = auto()
    guild = auto()
    newbie = auto()
    guest = auto()
    other = auto()
    blacklist = auto()
    

class EventPayloadAction(StrEnum):
    BUFF = auto()
    REMOVE = auto()
    RESTORE = auto()


guild_roles = (Roles.creator, Roles.leader, Roles.captain, Roles.officer, Roles.guild, Roles.newbie)

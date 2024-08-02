from vkbottle.framework.labeler import BotLabeler

from .datetime import now
from .formatters import format_name, format_profile_skills
from .math import commission_price, discount_price, pure_price


def get_labeler() -> BotLabeler:
    from main import bot
    return bot.labeler

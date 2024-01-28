from vkbottle import API
from vkbottle.bot import Bot, BotLabeler

from config import group_token, ALLOWED_CHATS, IGNORE_LIST

import ORM

from .rules import WhiteListRule

api = API(group_token)
labeler = BotLabeler()
labeler.auto_rules = [WhiteListRule(IGNORE_LIST, ALLOWED_CHATS)]


import handlers
handlers.dummy()

bot = Bot(token=group_token, labeler=labeler)

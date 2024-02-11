from vkbottle import API
from vkbottle.bot import Bot, BotLabeler

from config import group_token, ALLOWED_CHATS

import ORM

from .rules import WhiteListChatRule

api = API(group_token)
labeler = BotLabeler()
labeler.auto_rules = [WhiteListChatRule(ALLOWED_CHATS)]


import handlers
handlers.dummy()

bot = Bot(token=group_token, labeler=labeler)

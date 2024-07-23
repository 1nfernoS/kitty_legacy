from vkbottle import API
from vkbottle.bot import Bot, BotLabeler

from config import group_token, ALLOWED_CHATS

# noinspection PyUnresolvedReferences
import ORM

from .rules import WhiteListChatRule, HelpGroup
from .middlewares import RegisterMiddleware, LogCommandMiddleware

api = API(group_token)
labeler = BotLabeler()
labeler.vbml_ignore_case = True
labeler.message_view.register_middleware(RegisterMiddleware)
labeler.message_view.register_middleware(LogCommandMiddleware)
labeler.auto_rules = [WhiteListChatRule(ALLOWED_CHATS)]


bot = Bot(token=group_token, labeler=labeler)

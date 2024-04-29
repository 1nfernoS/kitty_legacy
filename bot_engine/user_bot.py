from vkbottle.tools.dev.mini_types.user import MessageMin
from vkbottle.user import UserLabeler

from bot_engine.rules import OverseerRule
from .middlewares import CheckBuffMiddleware

from resources import puzzles

from loguru import logger

user_labeler = UserLabeler()
user_labeler.message_view.register_middleware(CheckBuffMiddleware)


@user_labeler.private_message(OverseerRule(puzzles['buffs']['critical']))
async def critical_buff(msg: MessageMin):
    logger.info('Critical buff')
    return


@user_labeler.private_message(OverseerRule(puzzles['buffs']['success']))
async def ordinary_buff(msg: MessageMin):
    logger.info('Ordinary buff')
    return


@user_labeler.private_message(OverseerRule(puzzles['buffs']['possible']))
async def failed_buff(msg: MessageMin):
    logger.info('Failed buff')
    return

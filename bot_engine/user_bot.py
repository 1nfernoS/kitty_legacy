from vkbottle.tools.dev.mini_types.user import MessageMin
from vkbottle.user import UserLabeler

from vkbottle import User, API

from ORM import session, BuffCmd, BuffUser

from config import OVERSEER_BOT
from data_typings import BuffPayload

from bot_engine.rules import OverseerRule
from resources.items import buff_races_dict
from .middlewares import CheckBuffMiddleware

from resources import puzzles

from loguru import logger

user_labeler = UserLabeler()
user_labeler.message_view.register_middleware(CheckBuffMiddleware)


# TODO:
#  Change balance


@user_labeler.private_message(OverseerRule(puzzles['buffs']['critical']))
async def critical_buff(msg: MessageMin, user_id: int):
    logger.info(f'Critical buff on @id{user_id}')
    return


@user_labeler.private_message(OverseerRule(puzzles['buffs']['success']))
async def ordinary_buff(msg: MessageMin, user_id: int):
    logger.info(f'Ordinary buff on @id{user_id}')
    return


@user_labeler.private_message(OverseerRule(puzzles['buffs']['possible']))
async def failed_buff(msg: MessageMin, user_id: int, voices: int = 0):
    if voices:
        logger.info(f'Defended from target @id{user_id}')
    logger.info(f'Failed buff from buffer @id{user_id}')
    return


async def buff_loop(buff_data: BuffPayload):
    with session() as s:
        buffer: BuffUser | None = s.query(BuffUser).filter(
            BuffUser.buff_user_id == buff_data['from_id']).first()
        cmd: BuffCmd | None = s.query(BuffCmd).filter(BuffCmd.buff_cmd_id == buff_data['buff_id']).first()

    cmd_text: str = (cmd.buff_cmd_text
                     .replace('race1', buff_races_dict[buffer.buff_user_race1])
                     .replace('race2', buff_races_dict[buffer.buff_user_race2]))

    user = User(token=buffer.buff_user_token, labeler=user_labeler)
    user_api = API(buffer.buff_user_token)

    msg_to_fwd = await user_api.messages.get_by_conversation_message_id(peer_id=int(2e9 + buff_data['chat_id']),
                                                                        conversation_message_ids=buff_data['msg_id'])

    await user_api.messages.send(random_id=0,
                                 peer_id=OVERSEER_BOT,
                                 forward_messages=[msg_to_fwd.items[0].id],
                                 message=cmd_text)
    import asyncio
    for i in range(3 * 10):
        await asyncio.sleep(0.1)
        async for event in user.polling.listen():
            for update in event.get("updates", []):
                await user.loop.create_task(user.router.route(update, user.polling.api))
    return

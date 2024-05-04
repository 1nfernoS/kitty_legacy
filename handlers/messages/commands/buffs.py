from typing import List, Dict

from vkbottle import CtxStorage
from vkbottle.tools.dev.mini_types.bot import MessageMin

from data_typings.enums import RoleAccess
from resources.items import buff_classes_dict

from ORM import session, BuffUser

from bot_engine import labeler
from bot_engine.rules import AccessRule

from profile_api.user_requests import get_buffer_voices


@labeler.chat_message(AccessRule(RoleAccess.take_buffs), text=['апо', 'apo'])
async def buffers_apostol(msg: MessageMin):
    from resources.keyboards import apostol
    with session() as s:
        apostols: List[BuffUser] | None = s.query(BuffUser) \
            .filter(BuffUser.buff_user_is_active == 1,
                    BuffUser.buff_type_id == buff_classes_dict['apostol']).all()
    if not apostols:
        return await msg.answer("Мне жаль, но сейчас нет ни одного активного апостола")
    apostols_voices: Dict[int, int] = {buffer.buff_user_id: await get_buffer_voices(buffer.buff_user_profile_key,
                                                                                    buffer.buff_user_id,
                                                                                    buffer.buff_type_id)
                                       for buffer in apostols
                                       }

    if not any(list(apostols_voices.values())):
        return await msg.answer("Мне жаль, но сейчас нет ни одного апостола с голосами")

    for buffer in apostols:
        if not buffers_apostol[buffer.buff_user_id]:
            continue
        await msg.answer(f'Голоса: {apostols_voices[buffer.buff_user_id]}',
                         keyboard=apostol(buffer.buff_user_id,
                                          msg.conversation_message_id,
                                          buffer.buff_user_chat_id,
                                          buffer.buff_user_race1,
                                          buffer.buff_user_race2)
                         )
    return

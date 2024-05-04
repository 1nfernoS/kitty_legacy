from typing import List, Dict

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
        # noinspection PyTypeChecker
        apostols: List[BuffUser] = s.query(BuffUser) \
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


@labeler.chat_message(AccessRule(RoleAccess.take_buffs), text=['прокли', 'дебаф', 'дебафф', 'debuff', 'debuf'])
async def buffers_warlock(msg: MessageMin):
    from resources.keyboards import warlock
    with session() as s:
        # noinspection PyTypeChecker
        warlocks: List[BuffUser] = s.query(BuffUser) \
            .filter(BuffUser.buff_user_is_active == 1,
                    BuffUser.buff_type_id == buff_classes_dict['warlock']).all()
    if not warlocks:
        return await msg.answer("Мне жаль, но сейчас нет ни одного активного чернокнижника")
    warlocks_voices: Dict[int, int] = {buffer.buff_user_id: await get_buffer_voices(buffer.buff_user_profile_key,
                                                                                    buffer.buff_user_id,
                                                                                    buffer.buff_type_id)
                                       for buffer in warlocks
                                       }

    if not any(list(warlocks_voices.values())):
        return await msg.answer("Мне жаль, но сейчас нет ни одного чернокнижника с голосами")

    for buffer in warlocks:
        if not warlocks_voices[buffer.buff_user_id]:
            continue
        await msg.answer(f'Голоса: {warlocks_voices[buffer.buff_user_id]}',
                         keyboard=warlock(buffer.buff_user_id,
                                          msg.conversation_message_id,
                                          buffer.buff_user_chat_id)
                         )
    return


@labeler.chat_message(AccessRule(RoleAccess.take_buffs), text=['травма', 'травмы', 'очистка', 'trauma'])
async def buffers_paladin(msg: MessageMin):
    from resources.keyboards import paladin, crusader, light_inc
    with session() as s:
        # noinspection PyTypeChecker
        paladins: List[BuffUser] = s.query(BuffUser) \
            .filter(BuffUser.buff_user_is_active == 1,
                    BuffUser.buff_type_id == buff_classes_dict['paladin']).all()
        # noinspection PyTypeChecker
        crusaders: List[BuffUser] = s.query(BuffUser) \
            .filter(BuffUser.buff_user_is_active == 1,
                    BuffUser.buff_type_id == buff_classes_dict['crusader']).all()
        # noinspection PyTypeChecker
        light_incs: List[BuffUser] = s.query(BuffUser) \
            .filter(BuffUser.buff_user_is_active == 1,
                    BuffUser.buff_type_id == buff_classes_dict['light_inc']).all()

    paladins_buffers = [*paladins, *crusaders, *light_incs]
    if not any(paladins_buffers):
        return await msg.answer("Мне жаль, но сейчас нет ни одного активного паладина")

    buffer_voices: Dict[int, int] = {
        buffer.buff_user_id: await get_buffer_voices(buffer.buff_user_profile_key,
                                                     buffer.buff_user_id,
                                                     buffer.buff_type_id)
        for buffer in paladins_buffers
    }

    for buffer in paladins_buffers:
        if buffer in paladins:
            if not buffer_voices[buffer.buff_user_id]:
                continue
            kbd = paladin(buffer.buff_user_id,
                          msg.conversation_message_id,
                          buffer.buff_user_chat_id)
        if buffer in crusaders:
            kbd = crusader(buffer.buff_user_id,
                           msg.conversation_message_id,
                           buffer.buff_user_chat_id)
        if buffer in light_incs:
            kbd = light_inc(buffer.buff_user_id,
                            msg.conversation_message_id,
                            buffer.buff_user_chat_id)
        # noinspection PyUnboundLocalVariable
        await msg.answer(f'Голоса: {buffer_voices[buffer.buff_user_id]}',
                         keyboard=kbd)

    return

from typing import List, Dict

from vkbottle.tools.dev.mini_types.bot import MessageMin

from data_typings.enums import RoleAccess
from resources.items import buff_classes_dict

from ORM import session, BuffUser

from bot_engine import labeler
from bot_engine.rules import AccessRule, HelpGroup

from profile_api.user_requests import get_buffer_voices


@labeler.chat_message(HelpGroup('apostol'), AccessRule(RoleAccess.take_buffs), text=['апо', 'apo'])
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


@labeler.chat_message(HelpGroup('warlock'), AccessRule(RoleAccess.take_buffs),
                      text=['прокли', 'дебаф', 'дебафф', 'debuff', 'debuf'])
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


@labeler.chat_message(HelpGroup('paladin'), AccessRule(RoleAccess.take_buffs),
                      text=['травма', 'травмы', 'очистка', 'trauma'])
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


def _extract_url(url: str) -> Dict[str, str]:
    if '#' in url:
        args = url[url.find('#') + 1:]
    elif '?' in url:
        args = url[url.find('?') + 1:]
    else:
        raise RuntimeError('Can\'t find symbol to parse link')
    return {i.split('=')[0]: i.split('=')[1] for i in args.split('&')}


@labeler.private_message(HelpGroup('skip'), AccessRule(RoleAccess.bot_access),
                         text=['/buffer <link_1> <link_2>', '/buffer\n<link_1>\n<link_2>'])
async def buffer_register(msg: MessageMin, link_1: str, link_2: str):
    from vkbottle_types.codegen.objects import MessagesConversationPeerType
    from vkbottle import API
    from config import GUILD_CHAT_NAME
    
    msg_pit_err = 'Не могу найти ссылку на профиль колодца... Точно указал как в статье а не приложение вк?'
    
    if 'oauth.vk.com' in link_1:
        vk_data = _extract_url(link_1)
        if 'vip3.activeusers.ru/app.php' in link_2:
            pit_data = _extract_url(link_2)
        else:
            return await msg.answer(msg_pit_err)
    elif 'oauth.vk.com' in link_2:
        vk_data = _extract_url(link_2)
        if 'vip3.activeusers.ru/app.php' in link_1:
            pit_data = _extract_url(link_1)
        else:
            return await msg.answer(msg_pit_err)
    else:
        return await msg.answer('Не могу найти ссылку с токеном вк... Точно скопировал ее целиком?')
    
    if not int(pit_data['viewer_id']) == int(vk_data['user_id']) == msg.from_id:
        return await msg.answer('Что-то не сходится... Какая-то из ссылок не о тебе')
    
    from profile_api.user_requests import get_player_races, get_buff_class
    
    class_id = await get_buff_class(pit_data['auth_key'], int(pit_data['viewer_id']))
    if not class_id:
        return await msg.answer('Ты дал мне ПОЛНЫЙ доступ к ВК и Колодцу, не имея класс. способный накладывать '
                                'заклинания? \nЯ закрою глаза и забуду, но лучше так не делай')
    
    races = await get_player_races(pit_data['auth_key'], int(pit_data['viewer_id']))
    if len(races) > 2:
        return await msg.answer('У тебя сейчас больше 2 рас в профиле. Дождись окончания благословения и повтори '
                                'еще раз (достаточно просто скопировать отправленное сообщение)')
    try:
        race1, race2 = races
    except ValueError:
        race1, race2 = races[0], None
    
    chat_id: int | None = None
    try:
        buffer_api = API(vk_data['access_token'])
    except ...:
        return await msg.answer('Токен от ВК неправильный, может менялся пароль?')
    dialogues = await buffer_api.messages.get_conversations()
    chats = [i for i in dialogues.items if i.conversation.peer.type == MessagesConversationPeerType.CHAT]
    for chat in chats:
        if chat.conversation.chat_settings.title == GUILD_CHAT_NAME:
            chat_id = chat.conversation.peer.local_id
    # await buffer_api.http_client.close()
    del buffer_api
    
    if not chat_id:
        return await msg.answer('Не могу найти чат гильдии, ты точно в нем состоишь?')
    
    with session() as s:
    
        buffer: BuffUser | None = s.query(BuffUser).filter(BuffUser.buff_user_id == msg.from_id).first()
        if not buffer:
            buffer = BuffUser(vk_data['user_id'], True,
                              pit_data['auth_key'], vk_data['access_token'],
                              class_id, race1, race2, chat_id)
        else:
            buffer.buff_user_is_active = True
            buffer.buff_user_token = vk_data['access_token']
            buffer.buff_user_profile_key = pit_data['auth_key']
            buffer.buff_type_id = class_id
            buffer.buff_user_race1 = race1
            buffer.buff_user_race2 = race2
            buffer.buff_user_chat_id = chat_id
        s.add(buffer)
        s.commit()
    
    return await msg.answer('Отлично, теперь ты один из бафферов!')
    
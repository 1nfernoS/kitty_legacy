from vkbottle import CtxStorage
from vkbottle.tools.dev.mini_types.bot import MessageEventMin
from vkbottle_types.events import GroupEventType

from bot_engine import labeler, api, bot
from bot_engine.rules import ActionEventRule
from bot_engine.user_bot import buff_loop
from data_typings.enums import EventPayloadAction


@labeler.raw_event(GroupEventType.MESSAGE_EVENT, MessageEventMin, ActionEventRule(EventPayloadAction.REMOVE))
async def remove(event: MessageEventMin):
    await api.messages.delete(cmids=event.conversation_message_id, peer_id=event.peer_id, delete_for_all=True)
    return await event.show_snackbar('Done!')


@labeler.raw_event(GroupEventType.MESSAGE_EVENT, MessageEventMin, ActionEventRule(EventPayloadAction.BUFF))
async def buff(event: MessageEventMin):
    res = await event.show_snackbar('Hatova!')
    if CtxStorage().contains(event.payload['data']['from_id']):
        return await api.messages.edit(event.peer_id, 'Баффер занят, повторите позднее',
                                       conversation_message_id=event.conversation_message_id)
    else:
        CtxStorage().set(
            event.payload['data']['from_id'],
            {'payload': event.payload['data'], 'event': event}
        )

    await bot.loop.create_task(buff_loop(event.payload['data']))

    return res

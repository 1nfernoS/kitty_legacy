from vkbottle.tools.dev.mini_types.bot import MessageEventMin
from vkbottle_types.events import GroupEventType

from bot_engine import labeler, api
from bot_engine.rules import ActionEventRule
from data_typings.enums import EventPayloadAction


@labeler.raw_event(GroupEventType.MESSAGE_EVENT, MessageEventMin, ActionEventRule(EventPayloadAction.REMOVE))
async def remove(event: MessageEventMin):
    await api.messages.delete(cmids=event.conversation_message_id, peer_id=event.peer_id, delete_for_all=True)
    return await event.show_snackbar('Done!')

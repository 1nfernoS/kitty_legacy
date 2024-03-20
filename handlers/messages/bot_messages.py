from vkbottle.tools.dev.mini_types.bot import MessageMin

from ORM import session, LogsItems, Item
from bot_engine import labeler
from bot_engine.rules import OverseerRule
from data_typings.enums import ItemAction


@labeler.chat_message(OverseerRule(f"&#<emo1>;[id<user_id:int>|<name>], Вы положили на склад: &#<emo2>;<count:int>*<item_name>!\n"
                                   f"&#128275;Места на складе: <space:int>"))
async def put_log(msg: MessageMin, user_id: int, count: int, item_name: str):
    with session() as s:
        item: Item | None = s.query(Item).filter(Item.name == item_name).first()
    if not item:
        return  # TODO: log error
    LogsItems(user_id, ItemAction.PUT, 0, item.id, count).make_log()
    return


@labeler.chat_message(OverseerRule(f"&#<emo1>;[id<user_id:int>|<name>], Вы взяли со склада: &#<emo2>;<count:int>*<item_name>!\n"
                                   f"&#128275;Места на складе: <space:int>"))
async def take_log(msg: MessageMin, user_id: int, count: int, item_name: str):
    with session() as s:
        item: Item | None = s.query(Item).filter(Item.name == item_name).first()
    if not item:
        return  # TODO: log error
    LogsItems(user_id, ItemAction.TAKE, 0, item.id, count).make_log()
    return

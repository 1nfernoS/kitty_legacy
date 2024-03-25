from vkbottle.tools.dev.mini_types.bot import MessageMin

from ORM import session, LogsItems, Item, LogsMoney, User
from bot_engine import labeler
from bot_engine.rules import OverseerRule
from data_typings.enums import ItemAction, ChangeMoneyAction
from resources import emoji
from utils.formatters import balance_message_addition


@labeler.chat_message(OverseerRule(f"&#<emo1>;[id<user_id:int>|<name>], Вы положили на склад: "
                                   f"&#<emo2>;<count:int>*<item_name>!\n"
                                   f"&#128275;Места на складе: <space:int>"))
async def item_put(msg: MessageMin, user_id: int, count: int, item_name: str):
    with session() as s:
        item: Item | None = s.query(Item).filter(Item.name == item_name).first()
    if not item:
        return  # TODO: log error
    LogsItems(user_id, ItemAction.PUT, 0, item.id, count).make_log()
    return


@labeler.chat_message(OverseerRule(f"&#<emo1>;[id<user_id:int>|<name>], Вы взяли со склада: "
                                   f"&#<emo2>;<count:int>*<item_name>!\n"
                                   f"&#128275;Места на складе: <space:int>"))
async def item_take(msg: MessageMin, user_id: int, count: int, item_name: str):
    with session() as s:
        item: Item | None = s.query(Item).filter(Item.name == item_name).first()
    if not item:
        return  # TODO: log error
    LogsItems(0, ItemAction.TAKE, user_id, item.id, count).make_log()
    return


@labeler.chat_message(OverseerRule([f"&#<emo_item>;[id<id_to:int>|<name_to>], получено: "
                                    f"&#<emo>;<count:int>*<item_name> от игрока [id<id_from:int>|<name_from>]!",
                                    f"&#<emo_item>;[id<id_to:int>|<name_to>], получено: &#<emo>;<item_name>"
                                    f" от игрока [id<id_from:int>|<name_from>]!"]))
async def item_transfer(msg: MessageMin, id_from: int, id_to: int, item_name: str, count: int = 1):
    with session() as s:
        item: Item | None = s.query(Item).filter(Item.name == item_name).first()
    if not item:
        return  # TODO: log error
    LogsItems(id_from, ItemAction.GIVE, id_to, item.id, count).make_log()
    return


@labeler.chat_message(OverseerRule(f"{emoji.gold}[id<user_id>|<name>], Вы взяли <count:int> золота из казны."))
async def money_take(msg: MessageMin, user_id: int, count: int):
    LogsMoney(user_id, ChangeMoneyAction.SUB, count, 0, 'FROM STORAGE').make_log()
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == user_id).first()
        user.balance -= count
        s.add(user)
        s.commit()
        answer = f"О, [id{user_id}|Вы] взяли {count} золота!\n" + balance_message_addition(user.balance)
    return await msg.answer(answer)


@labeler.chat_message(OverseerRule(
    f"{emoji.gold}[id<user_id>|<name>], Вы положили <count:int> золота в казну (комиссия 10%)."))
async def money_put(msg: MessageMin, user_id: int, count: int):
    LogsMoney(user_id, ChangeMoneyAction.ADD, count, 0, 'TO STORAGE').make_log()
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == user_id).first()
        user.balance += count
        s.add(user)
        s.commit()
        answer = f"О, [id{user_id}|Вы] положили {count} золота!\n" + balance_message_addition(user.balance)
    return await msg.answer(answer)


@labeler.chat_message(OverseerRule(
    f'[id<user_id:int>|<name>], Ваш профиль:\n'
    f'&#128100;Класс: <class_name>, <races>\n'
    f'&#128101;Гильдия: <guild_name>\n'
    f'&#128519;<karma> карма\n'
    f'{emoji.level}Уровень: <level:int>\n'
    f'&#127881;Достижений: <achievements:int>\n'
    f'{emoji.gold}<gold:int> {emoji.scatter}<scatter:int>\n'
    f'{emoji.strength}<strength:int> {emoji.agility}<agility:int> {emoji.endurance}<endurance:int> '
    f'{emoji.luck}<luck:int> {emoji.attack}<attack:int> {emoji.defence}<defence:int>'))
async def profile_message(msg: MessageMin, user_id: int, name: str, class_name: str, races: str,
                          guild_name: str, karma: int, level: int, achievements: int,
                          gold: int, scatter: int,
                          strength: int, agility: int, endurance: int,
                          luck: int, attack: int, defence: int):
    # TODO
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == user_id).first()

        s.add(user)
        s.commit()

    return await msg.answer()

from typing import Dict, List

from vkbottle import VKAPIError, CtxStorage
from vkbottle.tools.dev.mini_types.bot import MessageMin

from ORM import session, LogsItems, Item, LogsMoney, User, Role
from bot_engine import labeler, api
from bot_engine.rules import OverseerRule, HelpGroup
from config import GUILD_NAME
import profile_api
from data_typings import CtxStorageData
from data_typings.enums import ItemAction, ChangeMoneyAction, Roles
from resources import emoji, items
from utils.formatters import balance_message_addition, date_diff, format_name
from utils.datetime import now


@labeler.chat_message(HelpGroup('item_storage'),
                      OverseerRule(f"&#<emo1>;[id<user_id:int>|<name>], Вы положили на склад: "
                                   f"&#<emo2>;<count:int>*<item_name>!\n"
                                   f"&#128275;Места на складе: <space:int>"))
async def item_put(msg: MessageMin, user_id: int, count: int, item_name: str):
    with session() as s:
        item: Item | None = s.query(Item).filter(
            Item.name.op('regexp')(f"(Книга - |Книга - [[:alnum:]]+ |^[[:alnum:]]+ |^){item_name}.*$"),
            Item.has_price == 1).first()
    if not item:
        return  # TODO: log error

    LogsItems(user_id, ItemAction.PUT, 0, item.id, count).make_log()

    if item.id not in items.ordinary_books_all:
        return

    price = await profile_api.get_price(item.id)
    if price <= 0:
        return

    with session() as s:
        # noinspection PyTypeChecker
        user: User = s.query(User).filter(User.user_id == user_id).first()
        user.balance += price * count
        s.add(user)
        s.commit()

        answer = f"{await format_name(user.user_id, 'nom')}, пополняю баланс на {price * count}{emoji.gold}"
        answer += f"({count}*{price})\n" if count > 1 else "\n" + balance_message_addition(user.balance)

    return await msg.answer(answer)


@labeler.chat_message(HelpGroup('item_storage'),
                      OverseerRule(f"&#<emo1>;[id<user_id:int>|<name>], Вы взяли со склада: "
                                   f"&#<emo2>;<count:int>*<item_name>!\n"
                                   f"&#128275;Места на складе: <space:int>"))
async def item_take(msg: MessageMin, user_id: int, count: int, item_name: str):
    with session() as s:
        item: Item | None = s.query(Item).filter(
            Item.name.op('regexp')(f"(Книга - |Книга - [[:alnum:]]+ |^[[:alnum:]]+ |^){item_name}.*$"),
            Item.has_price == 1).first()
    if not item:
        return  # TODO: log error

    LogsItems(0, ItemAction.TAKE, user_id, item.id, count).make_log()

    if item.id not in items.ordinary_books_all:
        return

    price = await profile_api.get_price(item.id)
    if price <= 0:
        return

    with session() as s:
        # noinspection PyTypeChecker
        user: User = s.query(User).filter(User.user_id == user_id).first()
        user.balance -= price * count
        s.add(user)
        s.commit()

        answer = f"{await format_name(user.user_id, 'nom')}, списываю с баланса {price * count}{emoji.gold}"
        answer += f"({count}*{price})\n" if count > 1 else "\n" + balance_message_addition(user.balance)

    return await msg.answer(answer)


# noinspection PyUnusedLocal
@labeler.chat_message(HelpGroup('item_transfer'),
                      OverseerRule([f"&#<emo_item>;[id<id_to:int>|<name_to>], получено: "
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


@labeler.chat_message(HelpGroup('item_storage'),
                      OverseerRule(f"{emoji.gold}[id<user_id>|<name>], Вы взяли <count:int> золота из казны."))
async def money_take(msg: MessageMin, user_id: int, count: int):
    LogsMoney(user_id, ChangeMoneyAction.SUB, count, 0, 'FROM STORAGE').make_log()
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == user_id).first()
        user.balance -= count
        s.add(user)
        s.commit()
        answer = f"{await format_name(user_id), 'nom'}, Вы взяли {count} золота!\n" + \
                 balance_message_addition(user.balance)
    return await msg.answer(answer)


@labeler.chat_message(HelpGroup('item_storage'),
                      OverseerRule(f"{emoji.gold}[id<user_id>|<name>], "
                                   f"Вы положили <count:int> золота в казну (комиссия 10%)."))
async def money_put(msg: MessageMin, user_id: int, count: int):
    LogsMoney(user_id, ChangeMoneyAction.ADD, count, 0, 'TO STORAGE').make_log()
    with session() as s:
        user: User | None = s.query(User).filter(User.user_id == user_id).first()
        user.balance += count
        s.add(user)
        s.commit()
        answer = f"{await format_name(user_id), 'nom'}, Вы положили {count} золота!\n" + \
                 balance_message_addition(user.balance)
    return await msg.answer(answer)


@labeler.chat_message(HelpGroup('profile'),
                      OverseerRule(
    f'[id<user_id:int>|<name>], Ваш профиль:\n'
    f'&#128100;Класс: <class_name>, <races>\n'
    f'&#128101;Гильдия: <guild_name>\n'
    f'&#<karma:int>;<karma_text> карма\n'
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
    msg_to_edit = await msg.answer('Читаю профиль...')

    class_name = class_name[:class_name.find(' (')] if ' (' in class_name else class_name
    in_guild = GUILD_NAME in guild_name
    new_role = Roles.other
    if emoji.officer in guild_name:
        new_role = Roles.officer
    elif in_guild:
        new_role = Roles.guild

    with session() as s:
        class_item: Item | None = s.query(Item).filter(Item.name.ilike(class_name)).first()
        user: User | None = s.get(User, user_id)

        answer = (f"[id{user_id}|{name}], статы обновлены! "
                  f"\n({date_diff(user.update_profile, now())}) "
                  f"\n(&#{karma};) {emoji.gold}: {gold} {emoji.scatter}: {scatter} {emoji.achievement}: {achievements}"
                  f"\nГильдия {guild_name} | {class_name} | {races}"
                  f"\n{emoji.level}{level}({level - user.stat_level}) {emoji.attack}{attack}"
                  f"({attack - user.stat_attack}) {emoji.defence}{defence}({defence - user.stat_defence})"
                  f"\n{emoji.strength}{strength}({strength - user.stat_strength}) "
                  f"{emoji.agility}{agility}({agility - user.stat_agility}) "
                  f"{emoji.endurance}{endurance}({endurance - user.stat_endurance})"
                  f"\n{emoji.luck}{luck}({luck - user.stat_luck})"
                  f"\n(До пинка {(level + 15) * 6 - strength - agility}{emoji.strength}/{emoji.agility} "
                  f"или {(level + 15) * 3 - endurance}{emoji.endurance})")

        user.class_id = class_item.id if class_item else user.class_id
        user.stat_level = level
        user.stat_attack = attack
        user.stat_defence = defence
        user.stat_luck = luck
        user.stat_strength = strength
        user.stat_agility = agility
        user.stat_endurance = endurance
        user.update_profile = now()

        if getattr(Roles, user.role_name) > new_role:
            user.role_name = new_role.name

        s.add(user)
        s.commit()

    msg_id = await api.messages.get_by_conversation_message_id(msg.peer_id, msg.conversation_message_id)
    try:
        await api.messages.delete(
            message_ids=msg_id.items[0].id,
            delete_for_all=True
        )
    except VKAPIError[15]:  # message from admin
        pass
    return await api.messages.edit(msg_to_edit.peer_id, answer,
                                   conversation_message_id=msg_to_edit.conversation_message_id)


@labeler.chat_message(HelpGroup('skip'),
                      OverseerRule(f"{emoji.item}[id<user_id:int>|<name>], "
                                   f"Вы получили со склада: <emoji><count:int>*<item_name>!"
                                   f"\n&#128275;Места на складе: <place:int"))
async def storage_item_get(msg: MessageMin, user_id: int, item_name: str, count: int):
    storage_ctx: Dict[int, List[CtxStorageData]] = CtxStorage().get('storage')
    requests: List[CtxStorageData] = storage_ctx.get(user_id, [])
    answer = ''
    if not requests:
        return
    for r in requests:
        if not (r['item_name'].replace('Книга - ', '').capitalize() == item_name.capitalize()
                and r['count'] == count):
            continue

        requests.remove(r)

        if 'Книга - ' not in r['item_name']:
            break
        item_price: int = await profile_api.get_price(r['item_id'])

        with session() as s:
            user: User | None = s.query(User).filter(User.user_id == user_id).first()
            if not user.user_role.can_balance:
                break

            user.balance -= count * item_price
            if count > 1:
                answer = (f"Выдал {count}*{item_name.capitalize()}, "
                          f"списываю с баланса {emoji.gold}{count * item_price}({count} * {emoji.gold}{item_price})")
            else:
                answer = f"Выдал {item_name.capitalize()}, списываю с баланса {emoji.gold}{count * item_price}"
            answer += f"\nОсталось на счету: {emoji.gold}{user.balance}"
            s.add(user)
            s.commit()
        break

    storage_ctx.update({user_id: requests})
    CtxStorage().set('storage', storage_ctx)

    if not answer:
        return
    else:
        return await msg.answer(answer)

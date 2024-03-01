from typing import List

from vkbottle.tools.dev.mini_types.bot import MessageMin
from vkbottle_types.objects import MessagesSendUserIdsResponseItem

from config import DISCOUNT_PERCENT
from data_typings.enums import RoleAccess
from data_typings.emoji import gold, tab
from utils.math import commission_price, discount_price
from utils.formatters import format_profile_skills

from bot_engine import labeler, api
from bot_engine.rules import AccessRule, FwdOrReplyUserRule

import profile_api
from profile_api.user_requests import get_profile, lvl_skills
from profile_api.formatters import get_books, get_build

from ORM import session, Item, User


async def _item_price_base(msg: MessageMin, item: str, count: int = 1) -> MessagesSendUserIdsResponseItem:
    if len(item) < 3:
        return await msg.answer('Добавьте пару букв к поиску, чтобы их было хотя бы 3')

    msg_to_edit = await msg.answer('Ищу ценники . . .')

    with session() as s:
        search: List[Item] = s.query(Item).filter(
            Item.name.op('regexp')(f"(Книга - |Книга - [[:alnum:]]+ |^[[:alnum:]]+ |^){item}.*$"),
            Item.has_price == 1).all()

    answer = ''
    cnt = 0
    for i in search:
        auc_price = await profile_api.get_price(i.id)
        if auc_price <= 0:
            continue

        guild_price = discount_price(auc_price)
        guild_commission_price = commission_price(guild_price)
        answer += f"\n{auc_price if count == 1 else auc_price * count}{gold} "
        answer += f"[-{DISCOUNT_PERCENT}%: {guild_price if count == 1 else guild_price * count}{gold}"
        answer += f"({guild_commission_price if count == 1 else guild_commission_price * count}{gold})] - "
        answer += f"{i.name}" if count == 1 else f"{count}*{i.name}"
        cnt += 1

    answer = f"Нашел следующее:" + answer if cnt > 0 else 'Ничего не нашлось...'

    return await api.messages.edit(msg_to_edit.peer_id, answer,
                                   conversation_message_id=msg_to_edit.conversation_message_id)


@labeler.message(AccessRule(RoleAccess.bot_access),
                 text=['цена <item:str> - <count:int>', 'price <item:str> - <count:int>'])
async def item_price_many(msg: MessageMin, item: str, count: int):
    try:
        count = int(count)
    except ValueError:
        return await msg.answer('Это не число')
    return await _item_price_base(msg, item, count)


@labeler.message(AccessRule(RoleAccess.bot_access), text=['цена <item>', 'price <item>'])
async def item_price(msg: MessageMin, item: str):
    return await _item_price_base(msg, item)


async def _get_build(user_id: int) -> str:
    with session() as s:
        auth: str | None = s.query(User.profile_key).filter(User.user_id == user_id).first()[0]
    if not auth:
        message = "Сдайте ссылку на профиль мне в лс!\n" \
                  "Проще всего это сделать через сайт, скопировав адрес ссылки кнопки 'Профиль' в приложении.\n" \
                  "Если получилась ссылка формата 'https:// vip3.activeusers .ru/блаблабла', то все получится)"
        return message

    profile = await get_profile(auth, user_id)
    inv = [int(i) for i in profile['items']]
    books = get_books(inv)
    build = get_build(inv)
    skills = await lvl_skills(auth, user_id)

    with session() as s:
        user: User = s.query(User).filter(User.user_id == user_id).first()
        user.user_items = [s.query(Item).filter(Item.id == i).first()
                           for i in books]
        s.add(user)
        s.commit()
    user_name = await api.users.get(user_id, name_case="gen")
    user_name = f"[id{user_name[0].id}|{user_name[0].first_name}]"
    message = f'Билд {user_name}:'
    if build['books']:
        message += '\nКниги:'
        message += format_profile_skills(build['books'], skills)

    if build['adms']:
        message += '\nВ адмах:'
        message += format_profile_skills(build['adms'], skills)

    return message

@labeler.message(AccessRule(RoleAccess.profile_app), text=['билд', 'build', 'экип', 'equip'])
async def get_self_build(msg: MessageMin):
    msg_to_edit = await msg.answer('Поднимаю записи...')

    message = await _get_build(msg.from_id)

    return await api.messages.edit(msg_to_edit.peer_id, message,
                                   conversation_message_id=msg_to_edit.conversation_message_id)


@labeler.message(FwdOrReplyUserRule(), AccessRule(RoleAccess.moderator),
                 text=['билд', 'build', 'экип', 'equip'])
async def get_other_build(msg: MessageMin):
    msg_to_edit = await msg.answer('Поднимаю записи...')

    target_id: int = msg.reply_message.from_id if msg.reply_message else msg.fwd_messages[0].from_id
    message = await _get_build(target_id)

    return await api.messages.edit(msg_to_edit.peer_id, message,
                                   conversation_message_id=msg_to_edit.conversation_message_id)

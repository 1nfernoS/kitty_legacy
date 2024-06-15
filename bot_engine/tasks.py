from typing import List, Dict
from json import loads
from datetime import timedelta, datetime

from sqlalchemy import func
from vkbottle import Keyboard, Callback, KeyboardButtonColor, VKAPIError
from vkbottle_types.codegen.objects import MessagesForward

from data_typings import RemindArgs, EventPayload, AnnounceRestorePayload

from config import GUILD_CHAT_ID, LEADER_CHAT_ID

from ORM import session, LogsElites, User, LogsSiege
from ORM.utils import Task, Announcements
from data_typings.enums import guild_roles, EventPayloadAction
from utils import now
from utils.formatters import format_name
from . import bot
from resources import emoji


async def elites(params: None = None):
    """
    Task to make monthly elites report
    Runs every month at 2nd day at 12:30
    """
    from . import api
    today = now().replace(hour=0, minute=0, second=0, microsecond=0)
    last_month = today.replace(year=today.year - 12 // (today.month + 11),
                               month=1 + (12 + today.month - 2) % 12)
    first_day = last_month.replace(day=1)
    last_day = first_day.replace(year=first_day.year + first_day.month // 12,
                                 month=first_day.month % 12 + 1)
    users = await api.messages.get_conversation_members(peer_id=2e9 + GUILD_CHAT_ID)
    with session() as s:
        elites_logs: Dict[int, int] = {user[0]: int(user[1]) for user in
                                       (s.query(LogsElites.user_id, func.sum(LogsElites.count))
                                        .filter(LogsElites.timestamp.between(first_day, last_day))
                                        .group_by(LogsElites.user_id).all())}
        # noinspection PyTypeChecker
        guild_users: Dict[int, int] = {u.user_id: u.stat_level for u in
                                       (s.query(User)
                                        .filter(User.role_name.in_(guild_roles)).all())}
    stats = {'more': 0, 'less': 0, 'equal': 0, 'none': 0}
    msg = f"Статистика по сдаче элитных трофеев за {now().strftime('%m.%Y')}\n\n"
    for user in users.items:
        if user.member_id < 0:
            continue
        if user.member_id in guild_users:
            continue
        user_level = guild_users.get(user.member_id, 0)

        if user_level == 0:
            continue
        elif user_level < 100:
            limit = 40
        elif user_level < 250:
            limit = 90
        else:
            limit = 120
        elites_count = elites_logs.get(user.user_id, 0)

        if elites_count > limit:
            stats['more'] += 1
            msg += emoji.check
        elif elites_count == limit:
            stats['equal'] += 1
            msg += emoji.check
        elif elites_count == 0:
            stats['none'] += 1
            msg += emoji.cancel
        elif elites_count < limit:
            stats['less'] += 1
            msg += emoji.cancel
        msg += (f"{await format_name(user.user_id, 'nom')}({user_level}): "
                f"{elites_count}/{limit}{emoji.elite_trophy}\n")
    msg += (f"\nИтого\n"
            f"Сверх нормы: {stats['more']}\n"
            f"Сдали ровно: {stats['equal']}\n"
            f"Недобрали: {stats['less']}\n"
            f"Не сдали ничего: {stats['none']}")
    await api.messages.send(chat_id=LEADER_CHAT_ID,
                            random_id=0,
                            message=msg,
                            disable_mentions=True
                            )
    next_execute = today.replace(year=today.year + today.month // 12,
                                 month=today.month % 12 + 1,
                                 day=2, hour=12, minute=30, second=0, microsecond=0)
    return next_execute


async def bill(params: None = None):
    """
    Task to make bill announcement
    Runs every month at 1st and 15th day at 10:30
    """
    from . import api
    today = now().replace(hour=0, minute=0, second=0, microsecond=0)
    await api.messages.send(chat_id=GUILD_CHAT_ID,
                            message='Сегодня будет списан налог!\n'
                                    'Все дружно написали "мой профиль" и "баланс" (без кавычек)\n\n@all',
                            random_id=0)
    if today.day > 1:
        next_execute = today.replace(day=1, month=today.month % 12 + 1, year=today.year + today.month // 12)
    else:
        next_execute = today.replace(day=15)
    return next_execute.replace(hour=10, minute=30, second=0, microsecond=0)


async def siege_stats(params: None = None):
    """
    Task to make siege stats report
    Runs every Wednesday at 22:05
    """
    from . import api
    today = now().replace(hour=0, minute=0, second=0, microsecond=0)
    users = await api.messages.get_conversation_members(peer_id=2e9 + GUILD_CHAT_ID)
    with session() as s:
        siege_logs: Dict[int, str] = {u.user_id: u.guild for u in
                                      s.query(LogsSiege)
                                      .filter(LogsSiege.timestamp >= today.date()).all()}
        guild_users: List[int] = [u.user_id for u in
                                  s.query(User)
                                  .filter(User.role_name.in_(guild_roles)).all()]
    msg = f"Статистика по осаде {today.strftime('%d.%m.%Y')}\n\n"
    frequent_guild = max(siege_logs.values(), key=lambda x: list(siege_logs.values()).count(x))
    stats = {'reported': 0, 'not_reported': 0, 'reported_wrong': 0}

    for user in users.items:
        if user.member_id not in guild_users:
            continue
        guild = siege_logs.get(user.member_id, None)
        if not guild:
            stats['not_reported'] += 1
            msg += f"{emoji.cancel} {await format_name(user.member_id, 'nom')}\n"
            continue

        if guild == frequent_guild:
            stats['reported'] += 1
        else:
            stats['reported_wrong'] += 1
        msg += f"{emoji.check} {await format_name(user.member_id, 'nom')} - {guild}\n"
    msg += (f"\nБольшая часть согильдийцев была в осаде на {frequent_guild}\n"
            f"{emoji.check}: {stats['reported']}; "
            f"{emoji.flag}: {stats['reported_wrong']}; "
            f"{emoji.cancel}: {stats['not_reported']}")

    await api.messages.send(chat_id=LEADER_CHAT_ID,
                            random_id=0,
                            message=msg,
                            disable_mentions=True
                            )
    next_run = today + timedelta(days=7 if today.isoweekday() == 3 else ((7 + 3 - today.isoweekday()) % 7))
    return next_run.replace(hour=22, minute=5, second=0, microsecond=0)


async def announcements(params: None = None):
    from . import api
    now_ = now()
    with session() as s:
        # noinspection PyTypeChecker
        messages: List[Announcements] = s.query(Announcements).filter(Announcements.is_active == 1).all()
    msg = f"{emoji.task} Объявления гильдии!"
    if not messages:
        msg += '\nТут пока пусто...'
    for message in messages:
        name = await format_name(message.note_author, 'nom')
        if message.expires_in < now_:
            message.remove()
            notify = (f'Ваше объявление {message.note_id} истекло - {message.note_text}\n'
                      f'Чтобы вернуть его нажмите кнопку ниже')

            data: AnnounceRestorePayload = {'note_id': message.note_id}
            payload: EventPayload = {'action': EventPayloadAction.RESTORE, 'data': data}
            kbd = Keyboard(inline=True)
            kbd.add(Callback('Восстановить', payload), KeyboardButtonColor.POSITIVE)

            try:
                await api.messages.send(peer_id=message.note_author,
                                        message=notify,
                                        random_id=0,
                                        keyboard=kbd.get_json())
            except VKAPIError[902, 901]:
                notify = f"{name}, разрешите сообщения, чтобы я уведомлял об этом в лс\n" + notify
                await api.messages.send(chat_id=GUILD_CHAT_ID,
                                        message=notify,
                                        random_id=0,
                                        keyboard=kbd.get_json())
            continue

        msg += f"\n -{emoji.tab}{name}: {message.note_text}"
    await api.messages.send(chat_id=GUILD_CHAT_ID,
                            random_id=0,
                            message=msg,
                            disable_mentions=True
                            )

    next_run = now_.replace(minute=0, second=0, microsecond=0) + timedelta(hours=2)
    return next_run


async def remind(params: RemindArgs):
    from . import api
    msg = f"{await format_name(params['user_id'], 'nom')}, напоминаю"
    if params['text']:
        msg += f":\n{params['text']}"
    fwd = MessagesForward(conversation_message_ids=[params['msg_id']],
                          peer_id=params['peer_id'],
                          is_reply=True).json()

    await api.messages.send(chat_id=GUILD_CHAT_ID,
                            random_id=0,
                            message=msg,
                            forward=fwd)
    return


@bot.loop_wrapper.interval(seconds=2)
async def check_tasks():
    now_ = now()
    with session() as s:
        # noinspection PyTypeChecker
        task_list: List[Task] = s.query(Task).filter(Task.task_active == 1).all()
        for task in task_list:
            if task.task_time_at > now_:
                continue
            next_time = await globals()[task.task_exec_target](loads(task.task_args) if task.task_args else None)
            if task.task_regular:
                if not isinstance(next_time, datetime):
                    raise AttributeError(
                        f"Task {task.task_exec_target} is regular, but no time for next call proceeded")
                task.task_time_at = next_time
            else:
                task.task_active = False
            s.add(task)
        s.commit()


async def ensure_tasks():
    today = now().replace(hour=0, minute=0, second=0, microsecond=0)
    regular_tasks = [
        Task(today.replace(year=today.year + today.month // 12,
                           month=today.month % 12 + 1,
                           day=2, hour=12, minute=30, second=0, microsecond=0),
             elites, None, True),
        Task(today.replace(year=today.year if today.day < 15 else today.year + today.month // 12,
                           month=today.month if today.day < 15 else today.month % 12 + 1,
                           day=15 if today.day < 15 else 1,
                           hour=10, minute=30, second=0, microsecond=0),
             bill, None, True),
        Task(today.replace(hour=22, minute=5, second=0, microsecond=0) +
             timedelta(days=7 if today.isoweekday() == 3
             else ((7 + 3 - today.isoweekday()) % 7)),
             siege_stats, None, True),
        Task(today.replace(hour=(now().hour//2)*2, minute=0, second=0, microsecond=0),
             announcements, None, True)
    ]
    with (session() as s):
        task_list: List[Task] = [task for task in
                                 (s.query(Task.task_exec_target)
                                  .filter(Task.task_active == 1).all())]
    for task in regular_tasks:
        if task.task_exec_target not in [i.task_exec_target for i in task_list]:
            task.add()
    return


bot.loop_wrapper.on_startup.append(ensure_tasks())

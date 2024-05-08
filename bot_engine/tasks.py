from typing import List, Dict
from json import loads
from datetime import timedelta, datetime

from sqlalchemy import func
from vkbottle_types.codegen.objects import MessagesForward

from data_typings import RemindArgs

from config import GUILD_CHAT_ID, LEADER_CHAT_ID

from ORM import session, LogsElites, User
from ORM.utils import Task
from data_typings.enums import guild_roles
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
    with session() as s:
        elites_logs: Dict[int, int] = {user[0]: int(user[1]) for user in
                                       (s.query(LogsElites.user_id, func.sum(LogsElites.count))
                                        .filter(LogsElites.timestamp.between(first_day, last_day))
                                        .group_by(LogsElites.user_id).all())}
        # noinspection PyTypeChecker
        guild_users: List[User] = (s.query(User)
                                   .filter(User.role_name.in_(guild_roles)).all())

    stats = {'more': 0, 'less': 0, 'equal': 0, 'none': 0}
    msg = f"Статистика по сдаче элитных трофеев за {now().strftime('%m.%Y')}\n\n"
    for user in guild_users:
        if user.stat_level < 100:
            limit = 40
        elif user.stat_level < 250:
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
        msg += (f"{await format_name(user.user_id, 'nom')}({user.stat_level}): "
                f"{elites_count}/{limit}{emoji.elite_trophy}\n")
    msg += (f"\nИтого\n"
            f"Сверх нормы: {stats['more']}\n"
            f"Сдали ровно: {stats['equal']}\n"
            f"Недобрали: {stats['less']}\n"
            f"Не сдали ничего: {stats['none']}")
    await api.messages.send(chat_id=LEADER_CHAT_ID,
                            random_id=0,
                            message=msg,
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
            next_time = await globals()[task.task_exec_target](loads(task.task_args))
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
             bill, None, True)
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

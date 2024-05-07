from typing import List
from json import loads
from datetime import timedelta

from vkbottle_types.codegen.objects import MessagesForward

from data_typings import RemindArgs

from config import GUILD_CHAT_ID

from ORM import session
from ORM.utils import Task

from utils.formatters import format_name
import utils
from . import bot


async def remind(params: RemindArgs):
    from . import api
    msg = f"{await format_name(params['user_id'], 'nom')}, напоминаю"
    if params['text']:
        msg += f":\n{params['text']}"
    fwd = MessagesForward(conversation_message_ids=[params['msg_id']],
                          peer_id=params['peer_id'],
                          is_reply=True).json()

    return await api.messages.send(chat_id=GUILD_CHAT_ID,
                                   random_id=0,
                                   message=msg,
                                   forward=fwd)


@bot.loop_wrapper.interval(seconds=2)
async def check_tasks():
    now = utils.now()
    with session() as s:
        # noinspection PyTypeChecker
        task_list: List[Task] = s.query(Task).filter(Task.task_active == 1).all()
        for task in task_list:
            if task.task_time_at > now:
                continue
            next_time = await globals()[task.task_exec_target](loads(task.task_args))
            if task.task_regular:
                if not isinstance(next_time, timedelta):
                    raise AttributeError(
                        f"Task {task.task_exec_target} is regular, but no time for next call proceeded")
                task.task_time_at = now + next_time
            else:
                task.task_active = False
            s.add(task)
        s.commit()

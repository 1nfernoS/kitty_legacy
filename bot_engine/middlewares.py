from vkbottle import BaseMiddleware, CtxStorage
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from ORM import session, BuffUser, User, LogsCommand
from data_typings import CtxBufferData

from config import OVERSEER_BOT

from resources.items import buff_classes_dict
from resources import emoji


class RegisterMiddleware(BaseMiddleware[BaseMessageMin]):
    """
    Middleware to check is user in DB.
    Register if not
    """

    async def pre(self):
        if self.event.from_id < 0:
            return
        from ORM import session, User
        with session() as s:
            user: User | None = s.query(User).filter(User.user_id == self.event.from_id).first()
            if not user:
                s.add(User(user_id=self.event.from_id))
                s.commit()
        return


class CheckBuffMiddleware(BaseMiddleware[BaseMessageMin]):
    """
    Middleware to check if user handlers were executed
    """

    async def post(self):
        if not self.handlers:
            return

        from loguru import logger
        from .user_bot import failed_buff, critical_buff, ordinary_buff

        self_user = await self.event.ctx_api.users.get()
        self_user = self_user[0]

        ctx_data: CtxBufferData = CtxStorage().get(self_user.id)
        ctx_event = ctx_data['event']
        ctx_payload = ctx_data['payload']

        from bot_engine import api as bot_api

        # noinspection PyTypeChecker
        target = await self.event.ctx_api.messages.get_by_conversation_message_id(
            peer_id=int(2e9 + ctx_payload['chat_id']),
            conversation_message_ids=ctx_payload['msg_id'])
        target_id = target.items[0].from_id

        with session() as s:
            target_user: User | None = s.query(User).filter(User.user_id == target_id).first()

            buffer: BuffUser | None = s.query(BuffUser).filter(BuffUser.buff_user_id == self_user.id).first()
            key = list(buff_classes_dict.keys())[list(buff_classes_dict.values()).index(buffer.buff_type_id)]
        # not format_name to avoid TooManyRequests Error
        answer = f"{getattr(emoji, key)} [id{self_user.id}|{self_user.first_name}]:\n"
        if failed_buff in self.handlers:
            logger.info('Failed')
            answer += f'{emoji.cancel}' + self.event.text.split(', ', 1)[-1]
        if critical_buff in self.handlers:
            logger.info('Critical')
            answer += (f'{emoji.luck}Критический баф!\n' +
                       self.event.text.split(emoji.luck)[0] +
                       f'\nОсталось на счету: {emoji.gold}{target_user.balance}')
        if ordinary_buff in self.handlers:
            logger.info('Ordinary')
            answer += (self.event.text.split('\n')[0] +
                       f'\nОсталось на счету: {emoji.gold}{target_user.balance}')
        await bot_api.messages.edit(peer_id=ctx_event.peer_id, message=answer,
                                    conversation_message_id=ctx_event.conversation_message_id,
                                    disable_mentions=True)

        CtxStorage().delete(self_user.id)
        import asyncio
        await asyncio.sleep(1)  # delay to avoid TooManyRequests Error
        await self.event.ctx_api.messages.mark_as_read(peer_id=OVERSEER_BOT)
        return


class LogCommandMiddleware(BaseMiddleware[BaseMessageMin]):
    """
    Middleware to log command if handler has been executed
    """

    async def post(self):
        if not self.handlers:
            return
        for handler in self.handlers:
            msg = self.event
            on_user_id = msg.fwd_messages[0].user_id if msg.fwd_messages \
                else msg.reply_message.from_user.id if msg.reply_message \
                else None
            on_user_text = msg.fwd_messages[0].text if msg.fwd_messages \
                else msg.reply_message.text if msg.reply_message \
                else None
            LogsCommand(self.event.from_id, str(handler), self.event.text, on_user_id, on_user_text).make_log()
        return

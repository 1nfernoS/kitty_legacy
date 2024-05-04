from vkbottle import BaseMiddleware, CtxStorage
from vkbottle.tools.dev.mini_types.base import BaseMessageMin

from data_typings import CtxBufferData


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
        if self.handlers:
            self_user = await self.event.ctx_api.users.get()
            self_user = self_user[0]

            ctx_data: CtxBufferData = CtxStorage().get(self_user.id)
            ctx_event = ctx_data['event']

            from bot_engine import api as bot_api
            await bot_api.messages.edit(peer_id=ctx_event.peer_id, message=self.event.text,
                                        conversation_message_id=ctx_event.conversation_message_id)

            CtxStorage().delete(self_user.id)
        return

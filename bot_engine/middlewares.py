from vkbottle import BaseMiddleware
from vkbottle.tools.dev.mini_types.base import BaseMessageMin


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
            from loguru import logger
            logger.info('Has buff answer')
        return

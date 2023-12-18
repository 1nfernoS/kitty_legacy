from vkbottle.tools.dev.mini_types.bot import MessageMin

from bot_engine import labeler

@labeler.message(text=['pong', 'понг'])
async def ping(msg: MessageMin):
    await msg.answer('ya jivoy xd')

import os

from vkbottle import ABCRule
from vkbottle.dispatch.rules.base import DEFAULT_PREFIXES
from vkbottle.bot import Message

class NotCommandRule(ABCRule[Message]):
    def __init__(self, prefixes: list = DEFAULT_PREFIXES):
        self.prefixes = prefixes

    async def check(self, message: Message) -> bool:
        return not any(message.text.startswith(prefix) for prefix in self.prefixes)


class ChitChatRule(ABCRule[Message]):
    def __init__(self):
        self.prefixes = ['/']

    async def check(self, message: Message) -> bool:
        has_prefix = any(message.text.startswith(prefix) for prefix in self.prefixes)
        from_bot = message.from_id < 0

        if has_prefix or from_bot:
            return False

        if message.peer_id == message.from_id:
            return True

        if os.getenv("BOT_NICKNAME") in message.text.lower():
            return True

        if message.reply_message:
            if message.reply_message.from_id == int(os.getenv("BOT_ID")):
                return True

        return False
    
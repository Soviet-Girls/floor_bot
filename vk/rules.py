from vkbottle import ABCRule
from vkbottle.bot import Message

from config import config

class ChitChatRule(ABCRule[Message]):
    def __init__(self):
        self.prefixes = ['/']

    async def check(self, message: Message) -> bool:
        has_prefix = any(message.text.startswith(prefix) for prefix in self.prefixes)
        from_bot = message.from_id < 0

        # if message.peer_id != config.vk.chat_peer_id:
        #     return False

        if has_prefix or from_bot:
            return False

        if message.peer_id == message.from_id:
            return True

        if "@sovietgirls_nft" in message.text.lower():
            return True

        if message.reply_message:
            if message.reply_message.from_id == -config.vk.group_id:
                return True

        return False
    
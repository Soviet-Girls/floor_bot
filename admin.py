# Проверка на админа беседы

from vkbottle.bot import Bot

async def check(bot: Bot, peer_id: int, user_id: int) -> bool:
    response = await bot.api.messages.get_conversation_members(peer_id=peer_id)
    for item in response.items:
        if item.member_id == user_id:
            if item.is_admin: return True
        else:
            return False
# Проверка на админа беседы

from vkbottle.bot import Bot

async def check(bot: Bot, peer_id: int, user_id: int) -> bool:
    try:
        response = await bot.api.messages.get_conversation_members(peer_id=peer_id)
    except Exception as e:
        await bot.api.messages.send(
            peer_id=peer_id, 
            message="Ошибка при получении списка участников беседы. Возможно, бот не администратор."
            )
        raise e
        
    for item in response.items:
        if item.member_id == user_id:
            return item.is_admin
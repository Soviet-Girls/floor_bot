# -*- coding: utf-8 -*-
# Проверка на админа беседы

# Импорт необходимых модулей
from config import config
from vkbottle.bot import Bot


# Создаем асинхронную функцию для проверки статуса администратора
async def check(bot: Bot, peer_id: int, user_id: int) -> bool:
    # Если пользователь является одним из заданных, возвращаем True
    if user_id in config.vk.admins:
        return True
    try:
        # Получаем список участников беседы
        response = await bot.api.messages.get_conversation_members(peer_id=peer_id)
    except Exception as e:
        # В случае ошибки отправляем сообщение об ошибке и прекращаем выполнение функции
        await bot.api.messages.send(
            peer_id=peer_id,
            message="Ошибка при получении списка участников беседы. Возможно, бот не является администратором."
        )
        raise e
    
    # Проходим по всем участникам беседы
    for item in response.items:
        # Если находим нужного пользователя, возвращаем его статус
        if item.member_id == user_id:
            return item.is_admin

    # Если пользователь не найден в списке участников, возвращаем False
    return False

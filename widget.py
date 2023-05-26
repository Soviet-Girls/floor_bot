import os
from vkbottle.bot import Bot
from floor import get_stats

community_bot = Bot(token=os.getenv("VK_WIDGET_KEY"))

async def generate_code():
    stats = await get_stats()
    widget = {
        "title": "Статистика коллекции",
        "title_url": "https://vk.com/wall-220643723_72",
        "more": "Перейти в маркетплейс",
        "more_url": "https://vk.com/wall-220643723_72",
        "head": [
            {"text": "Объем", "align": "center"},
            {"text": "Флор", "align": "center"},
            {"text": "Токенов", "align": "center"},
            {"text": "Владельцев", "align": "center"}
        ],
        "body": [
            [{"text": f"{stats['volume']} MATIC",},
            {"text": f"{stats['floorPrice']} MATIC"},
            {"text": f"{stats['items']}"},
            {"text": f"{stats['owners']}",}]
        ]
    }
    return f"return {widget};"

async def update():
    code = await generate_code()
    await community_bot.api.app_widgets.update(code=code, type="table")
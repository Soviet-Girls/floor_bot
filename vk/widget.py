from vkbottle.bot import Bot
from data.floor import get_stats

from config import config

community_bot = Bot(token=config.widget.token)


async def generate_code():
    stats = await get_stats()
    print(stats)
    widget = {
        "title": "Статистика коллекции",
        "title_url": config.widget.link,
        "more": "Перейти в маркетплейс",
        "more_url": config.widget.link,
        "head": [
            {"text": "Объем", "align": "center"},
            {"text": "Флор", "align": "center"},
            {"text": "Токенов", "align": "center"},
            {"text": "Владельцев", "align": "center"},
        ],
        "body": [
            [
                {
                    "text": f"{stats['volume']} MATIC",
                },
                {"text": f"{stats['floorPrice']} MATIC"},
                {"text": f"{stats['items']}"},
                {
                    "text": f"{stats['owners']}",
                },
            ]
        ],
    }
    return f"return {widget};"


async def update():
    code = await generate_code()
    await community_bot.api.app_widgets.update(code=code, type="table")

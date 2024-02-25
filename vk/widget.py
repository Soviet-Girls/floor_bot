from vkbottle.bot import Bot
from data.floor import get_stats, get_boys_stats
import data.currency as currency

from config import config

community_bot = Bot(token=config.widget.token)


# async def generate_code():
#     stats = await get_stats()
#     print(stats)
#     widget = {
#         "title": "Статистика коллекции",
#         "title_url": config.widget.link,
#         "more": "Перейти в маркетплейс",
#         "more_url": config.widget.link,
#         "head": [
#             {"text": "Объем", "align": "center"},
#             {"text": "Флор", "align": "center"},
#             {"text": "Токенов", "align": "center"},
#             {"text": "Владельцев", "align": "center"}
#         ],
#         "body": [
#             [
#                 {"text": f"{'%.2f' % float(stats['volume'])} MATIC"},
#                 {"text": f"{stats['floorPrice']} MATIC"},
#                 {"text": f"{stats['items']}"},
#                 {"text": f"{stats['owners']}"}
#             ]
#         ],
#     }
#     return f"return {widget};"

async def generate_code():
    stats_girls = await get_stats()
    stats_boys = await get_boys_stats()
    matic_rub, matic_usd = await currency.get_matic_rate()
    stats_girls['volume'] = "%.2f" % (stats_girls['volume'] * matic_rub / 1000)
    stats_boys['volume'] = "%.2f" % (stats_boys['volume'] * matic_rub / 1000)
    widget = {
        "title": "Статистика коллекции",
        "title_url": config.widget.link,
        "more": "Перейти в маркетплейс",
        "more_url": config.widget.link,
        "head": [
            {"text": "Коллекция"},
            {"text": "Объем", "align": "center"},
            {"text": "Флор", "align": "center"},
            {"text": "Токены", "align": "center"},
            {"text": "Владельцы", "align": "center"}
        ],
        "body": [
            [
                {"text": "♀️ Soviet Girls", "url": "https://vk.com/@sovietgirls_nft-about"},
                {"text": f"{stats_girls['volume']}К ₽"},
                {"text": f"{int(stats_girls['floorPrice']*matic_rub)} ₽"},
                {"text": f"{stats_girls['items']}"},
                {"text": f"{stats_girls['owners']}"}
            ],
            [
                {"text": "♂️ Soviet Boys", "url": "https://vk.com/@sovietgirls_nft-soviet-boys"},
                {"text": f"{stats_boys['volume']}К ₽"},
                {"text": f"{int(stats_boys['floorPrice']*matic_rub)} ₽"},
                {"text": f"{stats_boys['items']}"},
                {"text": f"{stats_boys['owners']}"}
            ],
            [
                {"text": "😺 Soviet Neko (скоро)", "url": "https://vk.com/wall-220643723_835"},
                {"text": f"-- ₽"},
                {"text": f"-- ₽"},
                {"text": f"322"},
                {"text": f"--"}
            ],
        ],
    }
    return f"return {widget};"


async def update():
    code = await generate_code()
    await community_bot.api.app_widgets.update(code=code, type="table")

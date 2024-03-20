from vkbottle.bot import Bot
from data.floor import get_stats, get_boys_stats
from vk.neko import get as get_neko
import data.currency as currency

from config import config

community_bot = Bot(token=config.widget.token)

girls_indicator = "👧"
boys_indicator = "👦"

old_girls_price = None
old_boys_price = None


def get_indicators(girls_price, boys_price):
    global old_girls_price, old_boys_price, girls_indicator, boys_indicator
    if old_girls_price is None or old_boys_price is None:
        old_girls_price = girls_price
        old_boys_price = boys_price
        return girls_indicator, boys_indicator
    if girls_price > old_girls_price:
        girls_indicator = "📈"
    elif girls_price < old_girls_price:
        girls_indicator = "📉"
    if boys_price > old_boys_price:
        boys_indicator = "📈"
    elif boys_price < old_boys_price:
        boys_indicator = "📉"
    old_girls_price = girls_price
    old_boys_price = boys_price
    return girls_indicator, boys_indicator


async def generate_code():
    stats_girls = await get_stats()
    stats_boys = await get_boys_stats()
    stats_neko = await get_neko()
    matic_rub, matic_usd = await currency.get_matic_rate()
    stats_girls["volume"] = "%.2f" % (stats_girls["volume"] * matic_rub / 1000)
    stats_boys["volume"] = "%.2f" % (stats_boys["volume"] * matic_rub / 1000)
    girl_emoji, boy_emoji = get_indicators(
        int(stats_girls["floorPrice"] * matic_rub),
        int(stats_boys["floorPrice"] * matic_rub),
    )
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
            {"text": "Владельцы", "align": "center"},
        ],
        "body": [
            [
                {
                    "text": f"{girl_emoji} Soviet Girls",
                    "url": "https://vk.com/@sovietgirls_nft-about",
                },
                {"text": f"{stats_girls['volume']}К ₽"},
                {"text": f"{int(stats_girls['floorPrice']*matic_rub)} ₽"},
                {"text": f"{stats_girls['items']}"},
                {"text": f"{stats_girls['owners']}"},
            ],
            [
                {
                    "text": f"{boy_emoji} Soviet Boys",
                    "url": "https://vk.com/@sovietgirls_nft-soviet-boys",
                },
                {"text": f"{stats_boys['volume']}К ₽"},
                {"text": f"{int(stats_boys['floorPrice']*matic_rub)} ₽"},
                {"text": f"{stats_boys['items']}"},
                {"text": f"{stats_boys['owners']}"},
            ],
            [
                {
                    "text": "😺 Soviet Neko (скоро)",
                    "url": "https://vk.com/wall-220643723_835",
                },
                {"text": stats_neko[0]},
                {"text": stats_neko[1]},
                {"text": "322"},
                {"text": stats_neko[2]},
            ],
        ],
    }
    return f"return {widget};"


async def update():
    code = await generate_code()
    await community_bot.api.app_widgets.update(code=code, type="table")

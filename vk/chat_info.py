import random
from vkbottle.bot import Bot
from data.floor import get_stats

from config import config

bot = Bot(token=config.vk.token)

cache_stats = {}


async def check_stats():
    global cache_stats

    stats = await get_stats()
    if stats == cache_stats:
        return
    
    print(stats)

    if stats["volume"] > cache_stats["volume"]:
        await bot.api.messages.send(
            peer_id=config.vk.chat_peer_id,
            message=f"📈 Объем: {stats['volume']} MATIC",
            random_id=random.randint(0, 2**64),
        )

    if stats["floorPrice"] != cache_stats["floorPrice"]:
        if stats["floorPrice"] < cache_stats["floorPrice"]:
            emoji = "📉"
        else:
            emoji = "📈"
        await bot.api.messages.send(
            peer_id=config.vk.chat_peer_id,
            message=f"{emoji} Флор: {stats['floorPrice']} MATIC",
            random_id=random.randint(0, 2**64),
        )

    if stats["items"] < cache_stats["items"]:
        await bot.api.messages.send(
            peer_id=config.vk.chat_peer_id,
            message=f"🔥 Токенов: {stats['items']}",
            random_id=random.randint(0, 2**64),
        )

    cache_stats = stats

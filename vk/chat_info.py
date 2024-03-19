import random
from vkbottle.bot import Bot
from data.floor import get_stats

from web3 import Web3
from web3.eth import AsyncEth

from config import config

w3 = Web3(
    Web3.AsyncHTTPProvider(config.rpc.address),
    modules={"eth": (AsyncEth,)},
    middlewares=[],
)

last_balance = None

bot = Bot(token=config.vk.token)

cache_stats = {}


async def check_stats():
    global cache_stats

    stats = await get_stats()
    if stats == cache_stats:
        return
    if cache_stats == {}:
        cache_stats = stats

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

async def get_balance():
    address = w3.to_checksum_address('0x63327acf277ba3d9aa309489ace95554279f8d8a')
    balance = await w3.eth.get_balance(address)
    # Convert to MATIC (1 MATIC = 10**18 wei)
    balance = float(w3.from_wei(balance, 'ether'))
    return balance

async def check_vknft():
    global last_balance
    balance = await get_balance()
    
    if last_balance is None:
        last_balance = balance
        return
    
    diff = balance - last_balance
    last_balance = balance
    if diff > 0:
        message = f"💰 Поступление на кошелек VK NFT Маркетплейса: {diff} MATIC\n"
        message += f"Баланс: {balance} MATIC\n\n"
        message += "https://polygonscan.com/address/0x63327acf277ba3d9aa309489ace95554279f8d8a\n@buvanenko"
        await bot.api.messages.send(
            peer_id=config.vk.chat_peer_id,
            message=message,
            random_id=random.randint(0, 2**64),
        )
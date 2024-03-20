from config import config
from vkbottle.bot import Bot


bot = Bot(token=config.vk.token)

async def set(text: str):
    value = text.split(" ")[0] + ' ₽'
    floor = text.split(" ")[1] + ' ₽'
    owners = text.split(" ")[2]

    await bot.api.storage.set(user_id=1, key="neko_value", value=value)
    await bot.api.storage.set(user_id=1, key="neko_floor", value=floor)
    await bot.api.storage.set(user_id=1, key="neko_owners", value=owners)

    return

async def get():
    value = await bot.api.storage.get(user_id=1, key="neko_value")
    floor = await bot.api.storage.get(user_id=1, key="neko_floor")
    owners = await bot.api.storage.get(user_id=1, key="neko_owners")
    if value == [] or floor == [] or owners == []:
        return "-- ₽", "-- ₽", "--"

    return value[0].value, floor[0].value, owners[0].value
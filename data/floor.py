# -*- coding: utf-8 -*-
# Получение флора

# Импорт необходимых модулей
import aiohttp
from config import config
from data.currency import get_matic_rate

headers = {"X-API-KEY": config.api.raribe_key}


# Функция для обработки запроса и получения данных от API Rarible
async def fetch_data(session, url):
    async with session.get(url) as resp:
        if resp.status != 200:
            print(f"Error: {resp.status}")
            data = await resp.json(content_type=None)
            print(f"Error: {data}")
            return None
        return await resp.json(content_type=None)


# Функция для получения флора и формирования сообщения
async def get():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            config.api.rarible + "floorPrice/?currency=MATIC", headers=headers
        ) as resp:
            data = await resp.json(content_type=None)
            if resp.status != 200:
                print(f"Error: {resp.status}")
                print(f"Error: {data}")
                return

    previous = data["historicalValues"][-1]
    change_percent = round((abs(data["currentValue"] - previous) / previous) * 100.0, 2)

    matic_rub, matic_usd = map(lambda x: round(x, 2), await get_matic_rate())

    currentRub = round(data["currentValue"] * matic_rub)

    if data["currentValue"] > previous:
        bot_message = f"📈 Актуальный флор: {data['currentValue']} MATIC (≈{currentRub}₽) [+{change_percent}%]"
    elif data["currentValue"] == previous:
        bot_message = (
            f"📊 Актуальный флор: {data['currentValue']} MATIC [≈{currentRub}₽]"
        )
    else:
        bot_message = f"📉 Актуальный флор: {data['currentValue']} MATIC (≈{currentRub}₽) [-{change_percent}%]"

    bot_message += f"\n\nВчера: {data['historicalValues'][-1]} MATIC"
    bot_message += f"\nПозавчера: {data['historicalValues'][-2]} MATIC"

    bot_message += f"\n\n1 MATIC ≈ {matic_rub}₽ | ${matic_usd}"

    return bot_message


async def get_stats():
    url = config.api.rarible + "stats/?currency=MATIC"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json(content_type=None)
            if resp.status != 200:
                print(f"Error: {resp.status}")
                print(f"Error: {data}")
                return
    return data


# Отдать голые данные
async def get_raw():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            config.api.rarible + "floorPrice/?currency=MATIC", headers=headers
        ) as resp:
            data = await resp.json(content_type=None)
            if resp.status != 200:
                print(f"Error: {resp.status}")
                print(f"Error: {data}")
                return
    return data

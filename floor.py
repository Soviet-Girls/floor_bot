# -*- coding: utf-8 -*-
# Получение флора

# Импорт необходимых модулей
import aiohttp
from config import config


# Функция для обработки запроса и получения данных от API Rarible
async def fetch_data(session, url):
    async with session.get(url) as resp:
        if resp.status != 200:
            print(f"Error: {resp.status}")
            data = await resp.json(content_type=None)
            print(f"Error: {data}")
            return None
        return await resp.json(content_type=None)
    

# Функция для получения данных о флоре и формирования сообщения
async def get():
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, config.api.rarible)
        if data is None:
            return

        previous = data["historicalValues"][-2]
        change_percent = round((abs(data["currentValue"] - previous) / previous) * 100.0, 2)

        if data["currentValue"] > previous:
            bot_message = f"📈 Актуальный флор: {data['currentValue']} MATIC (+{change_percent}%)"
        elif data["currentValue"] == previous:
            bot_message = f"📊 Актуальный флор: {data['currentValue']} MATIC"
        else:
            bot_message = f"📉 Актуальный флор: {data['currentValue']} MATIC (-{change_percent}%)"

        bot_message += f"\n\nВчера: {data['historicalValues'][-2]} MATIC"
        bot_message += f"\nПозавчера: {data['historicalValues'][-3]} MATIC"
        return bot_message


async def get_stats():
    url = config.api.rarible
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, url)
        if data is None:
            return
    return data


# Отдать сырые данные
async def get_raw():
    async with aiohttp.ClientSession() as session:
        data = await fetch_data(session, config.api.rarible)
        if data is None:
            return
    return data


# Функция для получения флора и формирования сообщения
async def get():
    async with aiohttp.ClientSession() as session:
        async with session.get(config.api.rarible) as resp:
            data = await resp.json(content_type=None)
            if resp.status != 200:
                print(f"Error: {resp.status}")
                print(f"Error: {data}")
                return

    previous = data["historicalValues"][-2]
    change_percent = round((abs(data["currentValue"] - previous) / previous) * 100.0, 2)

    if data["currentValue"] > previous:
        bot_message = (
            f"📈 Актуальный флор: {data['currentValue']} MATIC (+{change_percent}%)"
        )
    elif data["currentValue"] == previous:
        bot_message = f"📊 Актуальный флор: {data['currentValue']} MATIC"
    else:
        bot_message = (
            f"📉 Актуальный флор: {data['currentValue']} MATIC (-{change_percent}%)"
        )

    bot_message += f"\n\nВчера: {data['historicalValues'][-2]} MATIC"
    bot_message += f"\nПозавчера: {data['historicalValues'][-3]} MATIC"
    return bot_message

async def get_stats():
    url = config.api.rarible
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json(content_type=None)
            if resp.status != 200:
                print(f"Error: {resp.status}")
                print(f"Error: {data}")
                return
    return data


# Отдать голые данные
async def get_raw():
    async with aiohttp.ClientSession() as session:
        async with session.get(config.api.rarible) as resp:
            data = await resp.json(content_type=None)
            if resp.status != 200:
                print(f"Error: {resp.status}")
                print(f"Error: {data}")
                return
    return data

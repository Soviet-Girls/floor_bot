import os
import aiohttp


# Функция для получения флора и формирования сообщения
async def get():
    async with aiohttp.ClientSession() as session:
        async with session.get(os.getenv("RARIBLE_API_URL")) as resp:
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
        bot_message = f"📊 Актуальный флор: {data['currentValue']} MATIC)"
    else:
        bot_message = (
            f"📉 Актуальный флор: {data['currentValue']} MATIC (-{change_percent}%)"
        )

    bot_message += f"\n\nВчера: {data['historicalValues'][-2]} MATIC"
    bot_message += f"\nПозавчера: {data['historicalValues'][-3]} MATIC"
    return bot_message

async def get_stats():
    url = 'https://api.rarible.org/v0.1/data/collections/POLYGON:0x15f4272460062b835ba0abbf7a5e407f3ef425d3/stats/?currency=MATIC'
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
        async with session.get(os.getenv("RARIBLE_API_URL")) as resp:
            data = await resp.json(content_type=None)
            if resp.status != 200:
                print(f"Error: {resp.status}")
                print(f"Error: {data}")
                return
    return data

# -*- coding: utf-8 -*-
# Получение курса валют

# Импорт необходимых модулей
import aiohttp
from config import config
from typing import Tuple

import datetime
import xml.etree.ElementTree as ET

async def get_ton_rate():
    endpoint = 'https://tonapi.io/v2/rates?tokens=ton&currencies=ton%2Crub'
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint) as response:
            data = await response.json()
            return int(data['rates']['TON']['prices']['RUB'])

async def get_matic_rate() -> Tuple[float, float]:
    """
    Returns:
        Tuple[float, float]: A tuple containing the exchange rates of MATIC to RUB and USD.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            config.api.coinbase + "/exchange-rates?currency=MATIC"
        ) as response:
            data = await response.json()
            return float(data["data"]["rates"]["RUB"]), float(
                data["data"]["rates"]["USD"]
            )

async def get_matic_historical():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://tradingstrategy.ai/api/candles?pair_id=93754&exchange_type=uniswap_v2&time_bucket=1d"
        ) as response:
            data = await response.json()
    result = []
    for record in data["93754"][-5:]:
        result.append(record["c"])
    return result

async def get_ruble_usd_historical():
    date_req1 = (datetime.date.today() - datetime.timedelta(days=5)).strftime("%d/%m/%Y")
    date_req2 = datetime.date.today().strftime("%d/%m/%Y")
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_req1}&date_req2={date_req2}&VAL_NM_RQ=R01235"
        ) as response:
            data = await response.text()
    print(data)
    root = ET.fromstring(data)
    result = []
    for record in root:
        result.append(float(record[1].text.replace(",", ".")))
    return result

async def get_ruble_usd():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json(content_type=None)
    data = data['Valute']['USD']['Value']
    return data

async def get_matic_ruble_historical():
    matic_historical = await get_matic_historical()
    ruble_usd = await get_ruble_usd()
    result = []
    for i in range(5):
        result.append(matic_historical[i] * ruble_usd)
    return result
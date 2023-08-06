# -*- coding: utf-8 -*-
# Получение курса валют

# Импорт необходимых модулей
import aiohttp
from config import config
from typing import Tuple


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

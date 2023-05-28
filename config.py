# -*- coding: utf-8 -*-
# Загрузка переменных

# Импорт необходимых модулей
from dataclasses import dataclass
from environs import Env


@dataclass
class Collection:
    name: str
    address: str = None
    

@dataclass
class Markets:
    rarible: str = None
    opensea: str = None
    other: str = None


@dataclass
class APIs:
    rarible: str
    sber: str = "https://api.aicloud.sbercloud.ru/public/v2/boltalka/predict"


@dataclass
class VK:
    token: str
    admins: list
    bot_nick: str = None


@dataclass
class Config:
    nft: Collection
    markets: Markets
    api: APIs
    vk: VK


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        nft=Collection(
            name=env.str("COLLECTION_NAME", "КриптоКоллекция"),
            address=env.str("COLLECTION_ADDRESS", None),
        ),
        markets=Markets(
            rarible=env.str("MARKET_RARIBLE", None),
            opensea=env.str("MARKET_OPENSEA", None),
            other=env.str("MARKET_OTHER", None),
        ),
        api=APIs(
            rarible=env.str("API_RARIBLE"),
            sber=env.str("API_SBER", "https://api.aicloud.sbercloud.ru/public/v2/boltalka/predict"),
        ),
        vk=VK(
            token=env.str("VK_TOKEN"),
            admins=list(map(int, env.list("VK_ADMINS"))),
            bot_nick=env.str("VK_BOT_NICK", None),
        )
    )

config = load_config()
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
    coinbase: str = "https://api.coinbase.com/v2"


@dataclass
class VK:
    token: str
    admins: list


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
            coinbase=env.str("API_COINBASE", "https://api.coinbase.com/v2"),
        ),
        vk=VK(
            token=env.str("VK_TOKEN"),
            admins=list(map(int, env.list("VK_ADMINS"))),
        )
    )

config = load_config()
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
    raribe_key: str
    coinbase: str = "https://api.coinbase.com/v2"


@dataclass
class VK:
    token: str
    admins: list
    chat_peer_id: int = None
    group_id: int = 220643723


@dataclass
class Widget:
    token: str
    link: str


@dataclass
class OpenAI:
    api_key: str

@dataclass
class RPC:
    address: str


@dataclass
class Config:
    nft: Collection
    markets: Markets
    api: APIs
    vk: VK
    widget: Widget
    openai: OpenAI
    rpc: RPC


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
            raribe_key=env.str("RARIBLE_API_KEY"),
            coinbase=env.str("API_COINBASE", "https://api.coinbase.com/v2"),
        ),
        vk=VK(
            token=env.str("VK_TOKEN"),
            admins=list(map(int, env.list("VK_ADMINS"))),
            chat_peer_id=env.int("VK_CHAT_PEER_ID", None),
            group_id=env.int("VK_GROUP_ID", 220643723),
        ),
        widget=Widget(
            token=env.str("WIDGET_TOKEN"),
            link=env.str("WIDGET_LINK"),
        ),
        openai=OpenAI(
            api_key=env.str("OPENAI_API_KEY"),
        ),
        rpc=RPC(
            address=env.str("RPC_ADDRESS")
        )
    )


config = load_config()

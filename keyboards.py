# -*- coding: utf-8 -*-
# Пресеты клавиатур для сообщений

# Импорт необходимых модулей
from config import config
from vkbottle import Keyboard, OpenLink, Callback


def get_board():
    market_links = None
    # Создаем клавиатуру
    market_links = Keyboard(inline=True)

    # Если ссылка на дополнительный маркетплейс указана в конфигурации,
    # добавляем ее в клавиатуру
    if config.markets.other:
        market_links.add(OpenLink(link=config.markets.other, label="Маркетплейс"))
        market_links.row()  # Переходим на новую строку

    # Если ссылка на Rarible указана в конфигурации, добавляем ее в клавиатуру
    if config.markets.rarible:
        market_links.add(OpenLink(link=config.markets.rarible, label="Rarible"))

    # Если ссылка на OpenSea указана в конфигурации, добавляем ее в клавиатуру
    if config.markets.opensea:
        market_links.add(OpenLink(link=config.markets.opensea, label="OpenSea"))

    # Переходим на новую строку для следующей группы кнопок
    market_links.row()

    return market_links


def get_dm():
    # Получаем базовую клавиатуру
    market_links = get_board()

    # Добавляем кнопку обновления
    market_links.add(Callback("🔃 Обновить", payload={"command": "full_update"}))

    return market_links


def get_chat():
    # Получаем базовую клавиатуру
    market_links = get_board()

    # Добавляем кнопку обновления
    market_links.add(Callback("🔃 Обновить", payload={"command": "update"}))

    # Добавляем кнопку для отображения графика
    market_links.add(Callback("📈 График", payload={"command": "chart"}))

    return market_links

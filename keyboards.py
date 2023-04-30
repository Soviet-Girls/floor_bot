# Пресеты клавиатур для сообщений

from vkbottle import Keyboard, OpenLink

market_links = (
    Keyboard(inline=True)
    .add(OpenLink(link="https://rarible.com/Cryptospotty/", label="Rarible"))
    .add(OpenLink(link="https://opensea.io/collection/cryptospotty-1", label="OpenSea"))
)

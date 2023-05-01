# Пресеты клавиатур для сообщений

from vkbottle import Keyboard, OpenLink, Callback

market_links = (
    Keyboard(inline=True)
    .add(OpenLink(link="https://rarible.com/Cryptospotty/", label="Rarible"))
    .add(OpenLink(link="https://opensea.io/collection/cryptospotty-1", label="OpenSea"))
    .row()
    .add(Callback("🔃 Обновить", payload={"command": "update_full"}))
)


market_links_conversation = (
    Keyboard(inline=True)
    .add(OpenLink(link="https://rarible.com/Cryptospotty/", label="Rarible"))
    .add(OpenLink(link="https://opensea.io/collection/cryptospotty-1", label="OpenSea"))
    .row()
    .add(Callback("🔃 Обновить", payload={"command": "update"}))
    .add(Callback("📈 График", payload={"command": "chart"}))
)
# Пресеты клавиатур для сообщений

from vkbottle import Keyboard, OpenLink, Callback

market_links = (
    Keyboard(inline=True)
    .add(OpenLink(link="https://market.sovietgirls.su/", label="Маркетплейс"))
    .row()
    .add(OpenLink(link="https://rarible.com/sovietgirls/", label="Rarible"))
    .add(OpenLink(link="https://opensea.io/collection/sovietgirls", label="OpenSea"))
    .row()
    .add(Callback("🔃 Обновить", payload={"command": "update_full"}))
)


market_links_conversation = (
    Keyboard(inline=True)
    .add(OpenLink(link="https://market.sovietgirls.su/", label="Маркетплейс"))
    .row()
    .add(OpenLink(link="https://rarible.com/sovietgirls/", label="Rarible"))
    .add(OpenLink(link="https://opensea.io/collection/sovietgirls", label="OpenSea"))
    .row()
    .add(Callback("🔃 Обновить", payload={"command": "update"}))
    .add(Callback("📈 График", payload={"command": "chart"}))
)
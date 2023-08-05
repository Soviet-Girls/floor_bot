import random
from vkbottle.bot import Bot

from config import config
import data.nft as nft

async def start(bot: Bot):
    peer_id = config.vk.chat_peer_id

    # получить список участников беседы
    members = await bot.api.messages.get_conversation_members(peer_id=peer_id)
    members = members.items

    banlist = []
    wallets = {}

    for member in members:
        if member.member_id < 0: continue
        wallet = await bot.api.storage.get(key="wallet", user_id=member.member_id)
        wallet = wallet[0].value
        if wallet == "":
            banlist.append([member.member_id, "no wallet"])
            continue
        balance = await nft.balance_of(wallet)
        if balance == 0:
            banlist.append([member.member_id, "no NFT"])
            continue
        try:
            wallets[wallet].append(member.member_id)
        except KeyError:
            wallets[wallet] = [member.member_id]

    for wallet in wallets:
        if len(wallets[wallet]) > 1:
            for member_id in wallets[wallet]:
                banlist.append([member_id, "duplicate wallet"])

    for user_id, reason in banlist:
        if reason == "no wallet": reason = "отсутствие подключенного кошелька"
        elif reason == "duplicate wallet": reason = "дубликат кошелька"
        elif reason == "no NFT": reason = "отсутствие NFT из коллекции Soviet Girls"
        bot_message = f"Пользователь https://vk.com/id{user_id} забанен за {reason}.\n"
        bot_message += "Если вы считаете, что это ошибка, свяжитесь с администрацией сообщества."
        
        await bot.api.messages.send(
            peer_id=peer_id, 
            message=bot_message, 
            random_id=random.randint(0, 2 ** 64)
        )

        await bot.api.messages.remove_chat_user(chat_id=peer_id-2000000000, user_id=user_id)

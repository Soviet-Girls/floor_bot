from vkbottle.api import API
from config import config

api = API(config.vk_nft.token)

async def get_nfts(user_id):
    data = await api.request("nft.getCollection", {"owner_id": user_id})
    return data['response']['items']

async def check_nft(user_id: int, address: str):
    nfts = await get_nfts(user_id)
    for nft in nfts:
        if address.lower() in nft['nft_public_id'].lower():
            return True
    return False
import requests
from config import config

async def get_nfts(user_id):
    url = f"https://api.vk.com/method/nft.getCollection?access_token={config.vk_nft.token}&v=5.131&owner_id={user_id}"
    response = requests.get(url)
    data = response.json()
    return data['response']['items']

async def check_nft(user_id: int, address: str):
    nfts = await get_nfts(user_id)
    for nft in nfts:
        if address.lower() in nft['nft_public_id'].lower():
            return True
    return False
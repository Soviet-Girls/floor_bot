import aiohttp

query = """
query NftCollectionByAddress($address: String!, $userAddress: String!) {
  nftCollectionByAddress(address: $address) {
    approximateHoldersCount
    approximateItemsCount
    
  }
  alphaNftCollectionStats(address: $address) {
    floorPrice
    totalVolumeSold
  }
  userStats(userAddress: $userAddress) {
    tradingVolume
  }
}
"""

json_data = {
    'query': query,
    'variables': {
        "address": "EQBAS1oQQyLgHLTV7lg31yHT8FIbPM-Lsa2uMm8JDRi3WCwk",
        "userAddress": "EQBHxY02iPyaVa5KSqebug__2iL1ngT4PRCEIzPDFMKcUZqz"
    },
    'operationName': 'NftCollectionByAddress',
}

endpoint = "https://api.getgems.io/graphql"

async def get_stats():
    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, json=json_data) as resp:
            data = await resp.json(content_type=None)
            if resp.status != 200:
                print(f"Error: {resp.status}")
                print(f"Error: {data}")
                return
            
    volume = int(data['data']['alphaNftCollectionStats']['totalVolumeSold'])
    user_stats_volume = int(data['data']['userStats']['tradingVolume'])
    volume += user_stats_volume
    volume += 24 # получено с пресейла
    if volume == "0":
        volume = 0
    else:
        
        volume = int(str(volume)[:-9])

    stats = {
        'owners': int(data['data']['nftCollectionByAddress']['approximateHoldersCount']),
        'items': int(data['data']['nftCollectionByAddress']['approximateItemsCount']),
        'floor': int(data['data']['alphaNftCollectionStats']['floorPrice']),
        'volume': volume
    }
    return stats
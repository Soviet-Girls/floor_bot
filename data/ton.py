import aiohttp

query = """
query NftCollectionByAddress($address: String!) {
  nftCollectionByAddress(address: $address) {
    approximateHoldersCount
    approximateItemsCount
    
  }
  alphaNftCollectionStats(address: $address) {
    floorPrice
    totalVolumeSold
  }
}
"""

json_data = {
    'query': query,
    'variables': {
        'address': 'EQBAS1oQQyLgHLTV7lg31yHT8FIbPM-Lsa2uMm8JDRi3WCwk',
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
    stats = {
        'owners': int(data['data']['nftCollectionByAddress']['approximateHoldersCount']),
        'items': int(data['data']['nftCollectionByAddress']['approximateItemsCount']),
        'floor': int(data['data']['alphaNftCollectionStats']['floorPrice']),
        'volume': int(data['data']['alphaNftCollectionStats']['totalVolumeSold'])
    }
    return stats
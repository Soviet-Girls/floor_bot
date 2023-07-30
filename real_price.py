import aiohttp
import time

import tokens_on_address

traits = None
traits_price = None

async def get_items_by_collection(collection: str = "POLYGON:0x15f4272460062b835ba0abbf7a5e407f3ef425d3"):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.rarible.org/v0.1/items/byCollection?collection={collection}&size=10000") as response:
            return await response.json()
        

async def get_traits(
        collection: str = "POLYGON:0x15f4272460062b835ba0abbf7a5e407f3ef425d3", 
        traits_list: list = ['Hair', 'Background', 'Eyes', 'Hand raised', 'Headdress']
        ):
    
    global traits
    if traits:
        return traits
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.rarible.org/v0.1/items/traits?collectionIds={collection}&keys={','.join(traits_list)}") as response:
            response = await response.json()
    traits = {}
    for trait in response['traits']:
        for value in trait['values']:
            try:
                traits[trait['key']['value']].append({'value': value['value'], 'price': 0, 'count': value['count']})
            except KeyError:
                traits[trait['key']['value']] = []
                traits[trait['key']['value']].append({'value': value['value'], 'price': 0, 'count': value['count']})
    return traits

async def get_traits_price():
    global traits_price
    if traits_price and time.time() - traits_price['time'] < 60:
        return traits_price['traits']
    
    traits = await get_traits()
    items = await get_items_by_collection()
    try:
        items = items['items']
    except KeyError:
        print(items)
    for item in items: 
        try:
            price = float(item['bestSellOrder']['makePrice'])
        except KeyError:
            continue
        attributes = item['meta']['attributes']
        for attribute in attributes:
            for trait in traits[attribute['key']]:
                if trait['value'] == attribute['value']:
                    if trait['price'] > price or trait['price'] == 0:
                        trait['price'] = price
    traits_price = {'traits': traits, 'time': time.time()}
    return traits

async def get_item_floor_price(item_id: int, collection: str = "POLYGON:0x15f4272460062b835ba0abbf7a5e407f3ef425d3"):
    item_id = collection + ":" + str(item_id)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.rarible.org/v0.1/items/{item_id}") as response:
            response = await response.json()
    
    traits_price = await get_traits_price()

    price = 0
    traits = response['meta']['attributes']
    item_traits_price = []
    for trait in traits:
        for value in traits_price[trait['key']]:
            if value['value'] == trait['value']:
                item_traits_price.append({'key': trait['key'], 'value': trait['value'], 'price': value['price']})
                if value['price'] > price:
                    price = value['price']
                    largest_trait = {'key': trait['key'], 'value': trait['value']}
    return {'price': price, 'largest_trait': largest_trait, 'traits': item_traits_price}

async def get_balance(address):
    tokens = tokens_on_address.get(address)
    total_price = 0
    for token in tokens:
        price = await get_item_floor_price(token)
        total_price += price['price']
    return total_price
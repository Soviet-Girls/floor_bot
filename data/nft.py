# Получить количество NFT на аккаунте и их примерную стоимость

import data.floor as floor
import data.currency as currency

import data.real_price as real_price

import get_rpc


async def check_owner(address):
    w3, nft_contract = get_rpc.async_contract()
    try:
        address = w3.to_checksum_address(address)
        balance = await nft_contract.functions.balanceOf(address).call()
    except Exception as ex:
        raise ex
        return await check_owner(address)
    if balance > 0:
        return True
    return False


async def balance_of(address):
    w3, nft_contract = get_rpc.async_contract()
    try:
        address = w3.to_checksum_address(address)
        balance = await nft_contract.functions.balanceOf(address).call()
    except Exception as ex:
        raise ex
        return await balance_of(address)
    return balance


async def get_balance(address):
    # balance = await balance_of(address)
    # floor_price = await floor.get_raw()
    # floor_price = floor_price['currentValue']
    # matic_rub, matic_usd = await currency.get_matic_rate()
    # balance_matic = balance * floor_price
    # balance_rub = round(balance * floor_price * matic_rub, 2)
    # balance_usd = round(balance * floor_price * matic_usd, 2)

    balance = await real_price.get_balance(address)
    matic_rub, matic_usd = await currency.get_matic_rate()
    balance_matic = balance
    balance_rub = round(balance * matic_rub, 2)
    balance_usd = round(balance * matic_usd, 2)
    return balance, balance_matic, balance_rub, balance_usd

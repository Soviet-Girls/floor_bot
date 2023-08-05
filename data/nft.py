# Получить количество NFT на аккаунте и их примерную стоимость

import data.floor as floor
import data.currency as currency

import data.real_price as real_price

from web3 import Web3
from web3.eth import AsyncEth
import data.abi as abi

rpc_url = 'https://polygon.rpc.thirdweb.com'
chain_id = 137

w3 = Web3(Web3.AsyncHTTPProvider(rpc_url), modules={"eth": (AsyncEth,)}, middlewares=[])

nft_address = '0x15F4272460062b835Ba0abBf7A5E407F3EF425d3'
nft_contract = w3.eth.contract(nft_address, abi=abi.thirdweb)


async def check_owner(address):
    address = w3.to_checksum_address(address)
    balance = await nft_contract.functions.balanceOf(address).call()
    if balance > 0:
        return True
    return False

async def balance_of(address):
    address = w3.to_checksum_address(address)
    balance = await nft_contract.functions.balanceOf(address).call()
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
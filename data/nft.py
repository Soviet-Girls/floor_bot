# Получить количество NFT на аккаунте и их примерную стоимость

from web3 import Web3
from web3.eth import AsyncEth

import data.abi as abi
import data.floor as floor
import data.currency as currency

from config import config

w3 = Web3(
    Web3.AsyncHTTPProvider(config.rpc.address),
    modules={"eth": (AsyncEth,)},
    middlewares=[],
)
nft_contract = w3.eth.contract(
    "0x15F4272460062b835Ba0abBf7A5E407F3EF425d3", abi=abi.thirdweb
)


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


async def balance_of_neko(address):
    contract_address = w3.to_checksum_address('0xaebc78c7f624e4715ca436351f5ed9cb61e368bd')
    nft_contract = w3.eth.contract(
        contract_address, abi=abi.erc721
    )
    address = w3.to_checksum_address(address)
    balance = await nft_contract.functions.balanceOf(address).call()
    return balance


async def get_balance(address):
    balance = await balance_of(address)
    floor_price = await floor.get_raw()
    floor_price = floor_price["currentValue"]
    matic_rub, matic_usd = await currency.get_matic_rate()
    balance_matic = balance * floor_price
    balance_rub = round(balance_matic * matic_rub, 2)
    balance_usd = round(balance_matic * matic_usd, 2)
    return balance, balance_matic, balance_rub, balance_usd

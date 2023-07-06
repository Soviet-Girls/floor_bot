# Получить количество NFT на аккаунте и их примерную стоимость

import floor
import currency

from web3 import Web3
import abi

rpc_url = 'https://polygon.rpc.thirdweb.com'
chain_id = 137

w3 = Web3(Web3.HTTPProvider(rpc_url))

nft_address = '0x15F4272460062b835Ba0abBf7A5E407F3EF425d3'
nft_contract = w3.eth.contract(nft_address, abi=abi.thirdweb)

def check_owner(address):
    balance = nft_contract.functions.balanceOf(address).call()
    if balance > 0:
        return True
    return False

async def get_balance(address):
    address = Web3.to_checksum_address(address)
    balance = nft_contract.functions.balanceOf(address).call()
    floor_price = await floor.get_raw()
    floor_price = floor_price['currentValue']
    matic_rub, matic_usd = await currency.get_matic_rate()
    balance_matic = balance * floor_price
    balance_rub = balance * floor_price * matic_rub
    balance_usd = balance * floor_price * matic_usd
    return balance, balance_matic, balance_rub, balance_usd
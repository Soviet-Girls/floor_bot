# Получить количество NFT отправленных в стейкинг с аккаунта

from web3 import Web3
from web3.eth import AsyncEth

import data.abi as abi

from config import config

w3 = Web3(Web3.AsyncHTTPProvider(config.rpc.address), modules={"eth": (AsyncEth,)}, middlewares=[])
contract = w3.eth.contract("0xB24b7fb8750Cc8FD2B7c1e86d8FE55F3A279f64C", abi=abi.thirdweb_staking)

async def balance_of(address):
    address = w3.to_checksum_address(address)
    data = await contract.functions.getStakeInfo(address).call()
    return len(data[0])
# Получить количество NFT отправленных в стейкинг с аккаунта

from web3 import Web3
from web3.eth import AsyncEth

import data.abi as abi

from config import config

w3 = Web3(
    Web3.AsyncHTTPProvider(config.rpc.address),
    modules={"eth": (AsyncEth,)},
    middlewares=[],
)
contract = w3.eth.contract(
    "0xa877152a65D9F753bEB51d14f3176659fAB8F1Ad", abi=abi.thirdweb_erc20drop
)


async def balance_of(address):
    address = w3.to_checksum_address(address)
    data = await contract.functions.balanceOf(address).call()
    return int(w3.from_wei(data, "ether"))

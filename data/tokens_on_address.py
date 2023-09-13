from web3 import Web3
import concurrent.futures
from functools import partial

import data.abi as abi
from config import RPC

w3 = Web3(Web3.HTTPProvider(RPC.address), middlewares=[])
nft_contract = w3.eth.contract("0x15F4272460062b835Ba0abBf7A5E407F3EF425d3", abi=abi.thirdweb)

def get(address: str):
    total_supply = nft_contract.functions.totalSupply().call()
    total_supply = int(total_supply)
    tokens = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(total_supply):
            futures.append(
                executor.submit(
                    get_owner, partial(nft_contract.functions.ownerOf, i), i
                )
            )
        for future in concurrent.futures.as_completed(futures):
            owner, i = future.result()
            if owner and owner.lower() == address.lower():
                tokens.append(i)
    return tokens


def get_owner(ownerOf, i):
    try:
        owner = ownerOf().call()
    except:
        owner = None
    return owner, i

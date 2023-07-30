from web3 import Web3
import concurrent.futures

import abi

rpc_url = 'https://polygon.rpc.thirdweb.com'
chain_id = 137

w3 = Web3(Web3.HTTPProvider(rpc_url), middlewares=[])

nft_address = '0x15F4272460062b835Ba0abBf7A5E407F3EF425d3'
nft_contract = w3.eth.contract(nft_address, abi=abi.thirdweb)

def get(address: str):
    total_supply = nft_contract.functions.totalSupply().call()
    total_supply = int(total_supply)
    tokens = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(total_supply):
            futures.append(executor.submit(get_owner, i))
        for future in concurrent.futures.as_completed(futures):
            owner = future.result()
            if owner and owner.lower() == address.lower():
                tokens.append(i)
    return tokens

def get_owner(i):
    try:
        owner = nft_contract.functions.ownerOf(i).call()
    except:
        owner = None
    return owner
import random

from web3 import Web3
from web3.eth import AsyncEth
import data.abi as abi

rpc_list = [
    'https://polygon.llamarpc.com', 
    'https://polygon.blockpi.network/v1/rpc/public', 
    'https://polygon.rpc.blxrbdn.com', 
    'https://polygon-mainnet.public.blastapi.io', 
    'https://polygon-bor.publicnode.com', 
    'https://polygon-mainnet.g.alchemy.com/v2/demo', 
    'https://poly-rpc.gateway.pokt.network', 
    'https://rpc-mainnet.matic.quiknode.pro', 
    'https://polygon-mainnet.rpcfast.com?api_key=xbhWBI1Wkguk8SNMu1bvvLurPGLXmgwYeC4S6g2H7WdwFigZSmPWVZRxrskEQwIf', 
    'https://polygon-rpc.com', 
    'https://rpc-mainnet.maticvigil.com', 
    'https://1rpc.io/matic', 
    'https://endpoints.omniatech.io/v1/matic/mainnet/public', 
    'https://polygon.meowrpc.com', 
    'https://polygon.drpc.org', 
    'https://gateway.tenderly.co/public/polygon', 
    'https://polygon.gateway.tenderly.co', 
    'https://rpc.ankr.com/polygon', 
    'https://polygon.api.onfinality.io/public',
    'https://polygon.rpc.thirdweb.com'
    ]


def async_contract() -> tuple:
    w3 = Web3(Web3.AsyncHTTPProvider(random.choice(rpc_list)), modules={"eth": (AsyncEth,)}, middlewares=[])
    contract = w3.eth.contract("0x15F4272460062b835Ba0abBf7A5E407F3EF425d3", abi=abi.thirdweb)
    return w3, contract

def contract() -> tuple:
    w3 = Web3(Web3.HTTPProvider(random.choice(rpc_list)), middlewares=[])
    contract = w3.eth.contract("0x15F4272460062b835Ba0abBf7A5E407F3EF425d3", abi=abi.thirdweb)
    return w3, contract
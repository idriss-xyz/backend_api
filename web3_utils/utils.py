import os

from ens import ENS
from web3 import Web3

MAINNET_RPC = f"https://eth-mainnet.g.alchemy.com/v2/{os.getenv('ALCHEMY_API_KEY')}"

providerETHMain = Web3.HTTPProvider(MAINNET_RPC)

ns = ENS(providerETHMain)


def is_address(address):
    return Web3.is_address(address)

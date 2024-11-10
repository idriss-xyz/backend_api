from ens import ENS
from web3 import Web3

MAINNET_RPC = "https://eth.llamarpc.com"

providerETHMain = Web3.HTTPProvider(MAINNET_RPC)

ns = ENS(providerETHMain)

import os

import requests

from server_responses import HTTP_BAD_REQUEST, create_response
from utils.constants import (
    CUSD_ADDRESS,
    DEFAULT_TAKER,
    NATIVE_ADDRESS,
    PENGU_ON_ABSTRACT,
    USDC_ADDRESS_ON_ABSTRACT,
    USDC_ADDRESS_ON_ALEPH,
    USDC_ADDRESS_ON_CELO,
    USDC_ADDRESS_ON_RONIN,
    USDC_DECIMALS,
    UNSUPPORTED_0x_NETWORKS,
)
from utils.helper import get_token_router


def get_0x_token_pricing(network, sell_token, buy_token, sell_amount):
    if network in UNSUPPORTED_0x_NETWORKS:
        try:
            network, buy_token, sell_token = get_token_router(
                network, buy_token, sell_token
            )
        except KeyError as e:
            status_code = (
                e.response.status_code if hasattr(e, "response") else HTTP_BAD_REQUEST
            )
            return create_response({"error": "Token pair not supported"}, status_code)
    api_key = os.getenv("API_KEY_0X")
    url = (
        f"https://api.0x.org/swap/permit2/price"
        f"?chainId={network}"
        f"&sellToken={sell_token}"
        f"&buyToken={buy_token}"
        f"&sellAmount={sell_amount}"
        f"&taker={DEFAULT_TAKER}"
    )
    headers = {"0x-api-key": api_key, "0x-version": "v2"}

    try:
        api_response = requests.get(url, headers=headers, timeout=10)
        api_response.raise_for_status()
        return create_response(api_response.json(), api_response.status_code)
    except requests.RequestException as e:
        status_code = (
            e.response.status_code if hasattr(e, "response") else HTTP_BAD_REQUEST
        )
        return create_response({"error": str(e)}, status_code)


def get_alternative_token_price(network, sell_token, buy_token, sell_amount):
    if (
        network == "41455"
        and buy_token.lower() == NATIVE_ADDRESS
        and sell_token.lower() == USDC_ADDRESS_ON_ALEPH
    ):
        url = "https://api.diadata.org/v1/assetQuotation/AlephZero/0x0000000000000000000000000000000000000000"
        response = requests.get(url, timeout=5)
        data = response.json()
        latest_data = data["Price"]
        token_per_dollar = (float(sell_amount) / 10**USDC_DECIMALS) / float(latest_data)
        return {"price": token_per_dollar}
    elif (
        network == "2741"
        and buy_token.lower() == PENGU_ON_ABSTRACT
        and sell_token.lower() == USDC_ADDRESS_ON_ABSTRACT
    ):
        url = "https://hermes.pyth.network/v2/updates/price/latest?ids%5B%5D=0xbed3097008b9b5e3c93bec20be79cb43986b85a996475589351a21e67bae9b61"
        response = requests.get(url, timeout=5)
        data = response.json()
        latest_data = data["parsed"][0]["price"]["price"]
        token_per_dollar = (float(sell_amount) / 10**USDC_DECIMALS) / (
            float(latest_data) / 10**8
        )
        return {"price": token_per_dollar}
    elif (
        network == "2020"
        and buy_token.lower() == NATIVE_ADDRESS
        and sell_token.lower() == USDC_ADDRESS_ON_RONIN
    ):
        url = "https://hermes.pyth.network/v2/updates/price/latest?ids%5B%5D=0x97cfe19da9153ef7d647b011c5e355142280ddb16004378573e6494e499879f3"
        response = requests.get(url, timeout=5)
        data = response.json()
        latest_data = data["parsed"][0]["price"]["price"]
        token_per_dollar = (float(sell_amount) / 10**USDC_DECIMALS) / (
            float(latest_data) / 10**8
        )
        return {"price": token_per_dollar}
    elif (
        network == "42220"
        and buy_token.lower() == CUSD_ADDRESS
        and sell_token.lower() == USDC_ADDRESS_ON_CELO
    ):
        return {"price": 1}
    elif (
        network == "42220"
        and buy_token.lower() == NATIVE_ADDRESS
        and sell_token.lower() == USDC_ADDRESS_ON_CELO
    ):
        url = "https://hermes.pyth.network/v2/updates/price/latest?ids%5B%5D=0x7d669ddcdd23d9ef1fa9a9cc022ba055ec900e91c4cb960f3c20429d4447a411"
        response = requests.get(url, timeout=5)
        data = response.json()
        latest_data = data["parsed"][0]["price"]["price"]
        token_per_dollar = (float(sell_amount) / 10**USDC_DECIMALS) / (
            float(latest_data) / 10**8
        )
        return {"price": token_per_dollar}


def needs_alternative_pricing_route(network, sell_token, buy_token):
    if network == "41455" and buy_token.lower() == NATIVE_ADDRESS:
        return True
    if network == "2741" and buy_token.lower() == PENGU_ON_ABSTRACT:
        return True
    if network == "2020" and buy_token.lower() == NATIVE_ADDRESS:
        return True
    if network == "42220":
        return True
    return False

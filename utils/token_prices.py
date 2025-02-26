import os

import requests

from server_responses import HTTP_BAD_REQUEST, create_response
from utils.constants import (
    JIN_ON_RONIN,
    NATIVE_ADDRESS,
    PENGU_ON_ABSTRACT,
    PRICING_API_URL,
    USDC_ADDRESS_ON_ABSTRACT,
    USDC_ADDRESS_ON_ALEPH,
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
        f"{PRICING_API_URL[network]}/swap/v1/price"
        f"?sellToken={sell_token}"
        f"&buyToken={buy_token}"
        f"&sellAmount={sell_amount}"
    )
    headers = {"0x-api-key": api_key}

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
        total_amount = float(latest_data) * float(sell_amount) / 10**USDC_DECIMALS
        return {"price": token_per_dollar, "total_amount": total_amount}
    elif (
        network == "2020"
        and buy_token.lower() == JIN_ON_RONIN
        and sell_token.lower() == USDC_ADDRESS_ON_RONIN
    ):
        url = "https://api.roninchain.com/routing-api/prod/quote?tokenInChainId=2020&tokenInAddress=0x0B7007c13325C48911F73A2daD5FA5dCBf808aDc&tokenOutChainId=2020&tokenOutAddress=0xc340d3EdC4b11B56b5048991Aad5199659062f8C&amount=1000000&type=exactIn&enableUniversalRouter=true&enableFeeOnTransferFeeFetching=true&intent=quote&protocols=v3%2Cv2%2Cmixed&slippageTolerance=0.5"
        response = requests.get(url, timeout=5)
        data = response.json()
        token_per_dollar = data["quoteDecimals"]
        return {"price": token_per_dollar}


def needs_alternative_pricing_route(network, sell_token, buy_token):
    if network == "41455" and buy_token.lower() == NATIVE_ADDRESS:
        return True
    if network == "2741" and buy_token.lower() == PENGU_ON_ABSTRACT:
        return True
    if network == "2020" and (buy_token.lower() in [NATIVE_ADDRESS, JIN_ON_RONIN]):
        return True
    return False

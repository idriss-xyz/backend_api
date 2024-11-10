import os

import requests

from server_responses import HTTP_BAD_REQUEST, create_response
from utils.constants import (
    NATIVE_ADDRESS,
    PRICING_API_URL,
    USDC_ADDRESS_ON_ALEPH,
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
        total_amount = float(latest_data) * float(sell_amount) / 10**USDC_DECIMALS
        return {"price": token_per_dollar, "total_amount": total_amount}


def needs_alternative_pricing_route(network, sell_token, buy_token):
    if network == "41455" and buy_token == NATIVE_ADDRESS:
        return True
    return False

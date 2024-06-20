import os

import requests
from flask import Blueprint, make_response, request

from utils.constants import PRICING_API_URL, UNSUPPORTED_0x_NETWORKS
from utils.file_handler import fetch_agora_mock, fetch_custom_badges, fetch_handles
from utils.limiter import limiter
from utils.utils import get_token_router

extension_bp = Blueprint("extension", __name__)


# Add additional headers for extension context
@extension_bp.route('/token-price', methods=['GET', 'OPTIONS'])
@limiter.limit("10 per minute")
def get_token_price():
    if request.method == "OPTIONS":
        response = make_response({"message": "ok"}, 200)
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    sell_token = request.args.get("sellToken", None)
    buy_token = request.args.get("buyToken", None)
    sell_amount = request.args.get("sellAmount", None)
    network = request.args.get("network", "1")

    if not sell_token or not buy_token or not sell_amount:
        response = make_response({"error": "Missing required parameters"}, 400)
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    print(network, buy_token, sell_token)
    if network in UNSUPPORTED_0x_NETWORKS:
        try:
            network, buy_token, sell_token = get_token_router(network, buy_token, sell_token)
            print(network, buy_token, sell_token)
        except KeyError:
            status_code = e.response.status_code if hasattr(e, "response") else 400
            response = make_response({"error": "Token pair not supported"}, status_code)
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            return response

    api_key = os.getenv("API_KEY_0X")
    url = f"{PRICING_API_URL[network]}/swap/v1/price?sellToken={sell_token}&buyToken={buy_token}&sellAmount={sell_amount}"
    headers = {"0x-api-key": api_key}

    try:
        api_response = requests.get(url, headers=headers, timeout=10)
        api_response.raise_for_status()  # Will raise HTTPError for bad requests
        response = make_response(api_response.json(), api_response.status_code)
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    except requests.RequestException as e:
        status_code = e.response.status_code if hasattr(e, "response") else 400
        response = make_response({"error": str(e)}, status_code)
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response


@extension_bp.route('/fetch-agora', methods=["GET", "OPTIONS"])
@limiter.limit("20 per minute")
def fetch_agora():
    if request.method == "OPTIONS":
        response = make_response({"message": "ok"}, 200)
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    limit = request.args.get("limit", 1)
    offset = request.args.get("offset", 0)
    url = f'https://vote.optimism.io/api/v1/proposals?limit=${limit}&offset=${offset}'
    headers = {"bearerAuth ": os.getenv("API_KEY_AGORA")}

    try:
        # api_response = requests.get(url, headers=headers, timeout=10)
        # api_response.raise_for_status()
        # response = make_response(api_response.json(), api_response.status_code)
        ## MOCK START
        api_response = fetch_agora_mock()
        response = make_response(api_response, 200)
        ## MOCK END
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    except requests.RequestException as e:
        status_code = e.response.status_code if hasattr(e, "response") else 400
        response = make_response({"error": str(e)}, status_code)
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response


@extension_bp.route('/custom-badges', methods=["GET", "OPTIONS"])
def fetch_custom_twitter_badges():
    if request.method == "OPTIONS":
        response = make_response({"message": "ok"}, 200)
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    data = fetch_custom_badges()
    response = make_response(data, 200)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@extension_bp.route('/dao-handles', methods=["GET", "OPTIONS"])
@limiter.limit("20 per minute")
def fetch_dao_handles():
    if request.method == "OPTIONS":
        response = make_response({"message": "ok"}, 200)
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    data = fetch_handles()
    response = make_response(data, 200)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

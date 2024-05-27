import os
import requests
from flask import Blueprint, make_response, request

from utils.constants import UNSUPPORTED_0x_NETWORKS, PRICING_API_URL
from utils.utils import get_token_router
from utils.limiter import limiter

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

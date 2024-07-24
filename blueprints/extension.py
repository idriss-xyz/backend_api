import os

import requests
from flask import Blueprint, make_response, request

from utils.constants import PRICING_API_URL, TALLY_QUERY, UNSUPPORTED_0x_NETWORKS
from utils.file_handler import (
    fetch_agora_mock,
    fetch_custom_badges,
    fetch_gitcoin_rounds_by_chain,
    fetch_handles,
    get_status,
)
from utils.limiter import limiter
from utils.utils import get_token_router

extension_bp = Blueprint("extension", __name__)

@extension_bp.route("/service-status", methods=["GET", "OPTIONS"])
def return_service_status():
    """
    Allows to set up kill switches for services in our extension

    Returns:
        Response: A json response that indicates if a status from our extension is active or not.
    """
    print(request.headers)
    if request.method == "OPTIONS":
        response = make_response({"message": "ok"}, 200)
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    status = get_status()
    return status, 200


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


@extension_bp.route('/fetch-tally', methods=["GET", "OPTIONS"])
@limiter.limit("1 per second")
def fetch_tally():
    if request.method == "OPTIONS":
        response = make_response({"message": "ok"}, 200)
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    twitter_name = request.args.get('twitter-name')
    after_cursor = request.args.get('afterCursor', None)
    
    if not twitter_name:
        response = make_response({"error": "Missing required parameter: twitter-name."}, 400)
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response

    twitter_name = twitter_name.replace("@", "").lower()

    handles = fetch_handles()

    tally_organization_id = handles['tally'].get(twitter_name, None)
    if not tally_organization_id:
        response = make_response({"error": "No DAO associated with this handle."}, 404)
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    
    url = 'https://api.tally.xyz/query'
    variables = {
        "input": {
            "filters": {
            "includeArchived": False,
            "organizationId": tally_organization_id
            },
            "page": {
            "limit": 2,
            "afterCursor": after_cursor
            }
        }
    }
    data = {"operationName": "Proposals", "query": TALLY_QUERY, "variables": variables}
    headers = {"Api-Key": os.getenv("API_KEY_TALLY")}

    try:
        api_response = requests.post(url, json=data, headers=headers, timeout=60)
        api_response.raise_for_status()
        response_json = api_response.json()
        if "proposals" in response_json["data"]:
            response_json["data"]["proposalsV2"] = response_json["data"].pop("proposals")
        response = make_response(response_json, api_response.status_code)
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


@extension_bp.route('/gitcoin-rounds', methods=["GET", "OPTIONS"])
def fetch_gitcoin_rounds():
    if request.method == "OPTIONS":
        response = make_response({"message": "ok"}, 200)
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    data = fetch_gitcoin_rounds_by_chain()
    response = make_response(data, 200)
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@extension_bp.route('/dao-twitter-handles', methods=["GET", "OPTIONS"])
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

"""
Module for extension-related routes and utilities.

This module defines the Blueprint and routes for various endpoints used in the extension. 

Routes:
    /service-status (GET): Returns service status of extension addons.
    /token-price (GET): Retrieves token price based on provided parameters.
    /fetch-agora (GET): Fetches proposals from the Agora API.
    /fetch-tally (GET): Fetches proposals from the Tally API based on a Twitter handle.
    /custom-badges (GET): Fetches custom Twitter badges.
    /gitcoin-rounds (GET): Fetches Gitcoin rounds data.
    /dao-twitter-handles (GET): Fetches DAO Twitter handles.
    /post-data (POST): Validates a provided URL and fetches data from it.
    /fetch-image (GET): Fetches image from url and converts to base64.
"""


import os

import requests
from flask import Blueprint, make_response, request
from jsonschema import ValidationError, validate

from utils.constants import (
    FALLBACK_IMG_URL,
    PRICING_API_URL,
    TALLY_QUERY,
    UNSUPPORTED_0x_NETWORKS,
)
from utils.file_handler import (
    fetch_agora_mock,
    fetch_custom_badges,
    fetch_handles,
    get_status,
)
from utils.graph_ql import fetch_applications
from utils.limiter import limiter
from utils.responses import (
    HTTP_BAD_GATEWAY,
    HTTP_BAD_REQUEST,
    HTTP_OK,
    create_response,
    handle_options_request,
)
from utils.utils import fetch_data, get_token_router
from utils.validator import URL_SCHEMA

extension_bp = Blueprint("extension", __name__)

@extension_bp.route("/service-status", methods=["GET", "OPTIONS"])
def return_service_status():
    """
    Allows to set up kill switches for services in our extension

    Returns:
        Response: A json response that indicates if a status from our extension is active or not.
    """
    if request.method == "OPTIONS":
        return handle_options_request()
    
    status = get_status()
    return status, 200


@extension_bp.route('/token-price', methods=['GET', 'OPTIONS'])
@limiter.limit("10 per minute")
def get_token_price():
    """
    Retrieves token price using 0x API.

    Fetches the token price based on the provided sell token, buy token, and sell amount.

    Query Parameters:
        sellToken (str): The token to sell.
        buyToken (str): The token to buy.
        sellAmount (str): The amount of the sell token.
        network (str): The network ID (default is "1").

    Returns:
        Response: A JSON response containing the token price or an error message.
    """
    if request.method == "OPTIONS":
        return handle_options_request()
    
    sell_token = request.args.get("sellToken")
    buy_token = request.args.get("buyToken")
    sell_amount = request.args.get("sellAmount")
    network = request.args.get("network", "1")

    if not sell_token or not buy_token or not sell_amount:
        return create_response({"error": "Missing required parameters"}, HTTP_BAD_REQUEST)
    
    if network in UNSUPPORTED_0x_NETWORKS:
        try:
            network, buy_token, sell_token = get_token_router(network, buy_token, sell_token)
        except KeyError:
            status_code = e.response.status_code if hasattr(e, "response") else HTTP_BAD_REQUEST
            return create_response({"error": "Token pair not supported"}, status_code)

    api_key = os.getenv("API_KEY_0X")
    url = f"{PRICING_API_URL[network]}/swap/v1/price?sellToken={sell_token}&buyToken={buy_token}&sellAmount={sell_amount}"
    headers = {"0x-api-key": api_key}

    try:
        api_response = requests.get(url, headers=headers, timeout=10)
        api_response.raise_for_status() 
        return create_response(api_response.json(), api_response.status_code)
    except requests.RequestException as e:
        status_code = e.response.status_code if hasattr(e, "response") else HTTP_BAD_REQUEST
        return create_response({"error": str(e)}, status_code)


@extension_bp.route('/fetch-agora', methods=["GET", "OPTIONS"])
@limiter.limit("20 per minute")
def fetch_agora():
    """
    Fetches proposals from the Agora API.

    Query Parameters:
        limit (int): The number of proposals to retrieve (default is 1).
        offset (int): The offset for pagination (default is 0).

    Returns:
        Response: A JSON response containing the Agora data or an error message.
    """
    if request.method == "OPTIONS":
        return handle_options_request()
    
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
        return create_response(api_response, HTTP_OK)
        ## MOCK END
    except requests.RequestException as e:
        status_code = e.response.status_code if hasattr(e, "response") else HTTP_BAD_REQUEST
        return create_response({"error": str(e)}, status_code)


@extension_bp.route('/fetch-tally', methods=["GET", "OPTIONS"])
@limiter.limit("1 per second")
def fetch_tally():
    """
    Fetches data from the Tally API.

    Query Parameters:
        twitter-name (str): The Twitter handle of the DAO.
        afterCursor (str, optional): The cursor for pagination.

    Returns:
        Response: A JSON response containing the Tally data or an error message.
    """
    if request.method == "OPTIONS":
        return handle_options_request()
    
    twitter_name = request.args.get('twitter-name')
    after_cursor = request.args.get('afterCursor')
    
    if not twitter_name:
        return create_response({"error": "Missing required parameter: twitter-name."}, HTTP_BAD_REQUEST)

    twitter_name = twitter_name.replace("@", "").lower()

    handles = fetch_handles()

    tally_organization_id = handles['tally'].get(twitter_name)
    if not tally_organization_id:
        return create_response({"error": "No DAO associated with this handle."}, HTTP_BAD_REQUEST)
    
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
        return create_response(response_json, api_response.status_code)
    except requests.RequestException as e:
        status_code = e.response.status_code if hasattr(e, "response") else HTTP_BAD_REQUEST
        return create_response({"error": str(e)}, status_code)


@extension_bp.route('/custom-badges', methods=["GET", "OPTIONS"])
def fetch_custom_twitter_badges():
    """
    Fetches custom Twitter badges.

    Returns:
        Response: A JSON response containing custom badges data.
    """
    if request.method == "OPTIONS":
        return handle_options_request()
    
    data = fetch_custom_badges()
    return create_response(data, HTTP_OK)


@extension_bp.route('/gitcoin-rounds', methods=["GET"])
def fetch_gitcoin_rounds():
    """
    Endpoint to fetch Gitcoin rounds data.
    
    Returns:
        Response: A JSON response containing the applications data or an error message.
    """
    try:
        data = fetch_applications()
        return create_response(data, HTTP_OK)
    except requests.exceptions.RequestException as e:
        return create_response(
            {
                "error": "Failed to fetch data from Gitcoin GraphQL API",
                "details": str(e)
            },
            HTTP_BAD_GATEWAY
        )
    except KeyError as e:
        return create_response(
            {
                "error": "Unexpected response structure",
                "details": str(e)
            },
            HTTP_BAD_GATEWAY
        )
    except Exception as e:
        return create_response(
            {
                "error": "An unexpected error occurred",
                "details": str(e)
            },
            HTTP_BAD_REQUEST
        )


@extension_bp.route('/dao-twitter-handles', methods=["GET", "OPTIONS"])
@limiter.limit("20 per minute")
def fetch_dao_handles():
    """
    Fetches DAO Twitter handles.

    Returns:
        Response: A JSON response containing the DAO Twitter handles.
    """
    if request.method == "OPTIONS":
        return handle_options_request()
    
    data = fetch_handles()
    return create_response(data, HTTP_OK)


@extension_bp.route("/post-data", methods=["POST", "OPTIONS"])
def post_page():
    """
    Handles POST requests to fetch data from a given URL and validates the URL structure.

    This endpoint accepts JSON data containing a URL and validates it against predefined schemas.

    Returns:
        Response: A Flask response object with the fetched data or an error message.

    Raises:
        ValidationError: If the input data does not conform to the schema.
        requests.RequestException: If there is an error while making the request to the URL.
        Exception: For general exceptions during processing.

    Example JSON Request Body:
    {
        "url": "https://across.to/api/suggested-fees?originChainId=1&token=0x123...&amount=1000000000&message=example&recipient=0xabc...&destinationChainId=2"
    }
    """
    if request.method == "OPTIONS":
        return create_response("POST, OPTIONS")
    
    request_data = request.get_json()
    try:
        validate(instance=request_data, schema=URL_SCHEMA)
    except ValidationError as e:
        return create_response({"error": f"Invalid input: {e.message}"}, HTTP_BAD_REQUEST)  
    page_url = request_data.get("url")
    if not page_url:
        return create_response({"error": "No URL provided"}, HTTP_BAD_REQUEST)
    try:
        return fetch_data(page_url, "json")
    except requests.RequestException as e:
        status_code = e.response.status_code if hasattr(e, "response") else HTTP_BAD_REQUEST
        return create_response({"error": str(e)}, status_code)
    except Exception as e:
        status_code = e.response.status_code if hasattr(e, "response") else HTTP_BAD_REQUEST
        return create_response({"error": "Unable to process the image"}, status_code)
    

@extension_bp.route("/fetch-image", methods=["GET"])
def fetch_image():
    """
    Retrieve an image from a specified URL passed via query parameters.
    If the URL is not provided or an error occurs during the fetch, a fallback image is served.
    ToDo: Change fallback image based on param.

    Returns:
        base64 representation of requested image.
    """
    image_url = request.args.get("url")
    if not image_url:
        return create_response({"error": "No URL provided"}, HTTP_BAD_REQUEST)

    try:
        return fetch_data(image_url, "blob")
    except requests.RequestException:
        return fetch_data(FALLBACK_IMG_URL, "blob")

    except Exception:
        return fetch_data(FALLBACK_IMG_URL, "blob")

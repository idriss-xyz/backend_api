import base64

import requests

from utils.constants import DEFAULT_NETWORK, TOKEN_ROUTE
from utils.responses import HTTP_NOT_FOUND, HTTP_OK, create_response


def get_token_router(network, buy_token, sell_token):
    sell_token = TOKEN_ROUTE[f"{network}:{sell_token.lower()}"]
    buy_token = TOKEN_ROUTE[f"{network}:{buy_token.lower()}"]
    network = DEFAULT_NETWORK
    return network, buy_token, sell_token


def fetch_data(url, return_type):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    if return_type == "json":
        return create_response(response.json(), HTTP_OK)
    
    if return_type == "text":
        return create_response({"text": response.text}, HTTP_OK)
    
    if return_type == "blob":
        content_type = response.headers.get("content-type", "image/jpeg")
        img_base64 = base64.b64encode(response.content).decode()
        data_url = f"data:{content_type};base64,{img_base64}"
        return create_response({"image": data_url}, HTTP_OK)
    
    return create_response({}, HTTP_NOT_FOUND)
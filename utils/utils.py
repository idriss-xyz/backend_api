import base64
from io import BytesIO

import requests

from utils.constants import DEFAULT_NETWORK, TOKEN_ROUTE
from utils.responses import HTTP_NOT_FOUND, HTTP_OK, create_response

# from PIL import Image



def get_token_router(network, buy_token, sell_token):
    sell_token = TOKEN_ROUTE[f"{network}:{sell_token.lower()}"]
    buy_token = TOKEN_ROUTE[f"{network}:{buy_token.lower()}"]
    network = DEFAULT_NETWORK
    return network, buy_token, sell_token


def fetch_data(url, return_type):
    response = requests.get(url, timeout=10)
    if return_type == "json":
        return create_response(response.json(), HTTP_OK)
    if return_type == "text":
        response.raise_for_status()
        return create_response({"text": response.text}, HTTP_OK)
    # if return_type == "blob":
    #     response.raise_for_status()
    #     content_type = response.headers.get("content-type", "image/jpeg")
    #     image = Image.open(BytesIO(response.content))
    #     buffered = BytesIO()
    #     image_format = image.format if image.format else "JPEG"
    #     image.save(buffered, format=image_format)
    #     img_base64 = base64.b64encode(buffered.getvalue()).decode()
    #     data_url = f"data:{content_type};base64,{img_base64}"
    #     return create_response({"image": data_url}, HTTP_OK)
    return create_response({}, HTTP_NOT_FOUND)
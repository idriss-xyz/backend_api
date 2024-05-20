import os

import requests
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from utils.constants import PRICING_API_URL, UNSUPPORTED_0x_NETWORKS
from utils.utils import get_token_router

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


limiter = Limiter(
    get_remote_address,
    storage_uri="memory://"
)

limiter.init_app(app)


@app.route('/')
def hello_world():
    return jsonify(message="Hello, API!")


@app.route('/get-connected-addresses', methods=['GET'])
def get_fc():
    fid = request.args.get('fid')
    
    if not fid:
        return jsonify({'error': 'Missing fid parameter'}), 400

    url = f"https://api.warpcast.com/v2/verifications?fid={fid}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 400
    
    return jsonify(response.json())


@app.route('/get-twitter-id', methods=['GET'])
@limiter.limit("30 per minute")
def get_twitter():
    identifier = request.args.get('identifier').replace('@', '')
    
    if not identifier:
        return jsonify({'error': 'Missing identifier parameter'}), 400

    url = f"https://www.idriss.xyz/v1/getTwitterIDPlugin?usernames={identifier}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 400
    print(response.json())
    response_json = response.json()
    formatted_response = {'id': response_json['twitterIDs'].get(identifier, "Not found")}
    print(formatted_response)
    return jsonify(formatted_response), 200


@app.route('/resolve-unstoppable-domains', methods=['GET'])
@limiter.limit("10 per minute")
def get_ud():
    domain = request.args.get('domain')
    
    if not domain:
        return jsonify({'error': 'Missing identifier parameter'}), 400

    url = f"https://api.unstoppabledomains.com/resolve/domains/{domain}"
    try:
        response = requests.get(url, headers={'accept': 'application/json', 'authorization': f'Bearer {os.getenv("UD_API_KEY")}'})
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 400
    response_json = response.json()
    return jsonify(response_json), 200


# Add additional headers for extension context
@app.route('/token-price', methods=['GET', 'OPTIONS'])
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
    
    
if __name__ == '__main__':
    app.run(debug=True)

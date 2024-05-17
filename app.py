import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


limiter = Limiter(
    get_remote_address,
    storage_uri="memory://"
)

limiter.init_app(app)


@app.route('/')
def hello_world():
    return jsonify(message="Hello, world!")


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
    if response_json['twitterIDs'] == {}:
        formatted_response = {'id': 'Not found'}
    formatted_response = {'id': response_json['twitterIDs'][identifier]}
    print(formatted_response)
    return jsonify(formatted_response), 200
    
if __name__ == '__main__':
    app.run(debug=True)

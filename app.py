import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return jsonify(message="Hello, world!")

@app.route('/get-connected-addresses', methods=['GET'])
def verify():
    fid = request.args.get('fid')
    
    if not fid:
        return jsonify({'error': 'Missing fid parameter'}), 400

    url = f"https://api.warpcast.com/v2/verifications?fid={fid}"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 400
    
    response = jsonify(response.json())
    if 'Origin' in request.headers and request.headers['Origin'] == 'null':
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response
    
if __name__ == '__main__':
    app.run(debug=True)

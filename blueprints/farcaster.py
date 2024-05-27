import jsonify
import requests

from flask import Blueprint, request
from utils.farcaster import get_farcaster_verified_addresses

farcaster_bp = Blueprint("fc", __name__)

@farcaster_bp.route("/get-connected-addresses", methods=["GET"])
def get_fc_connected_addresses():
    fid = request.args.get('fid')
    
    if not fid:
        return jsonify({'error': 'Missing fid parameter'}), 400

    try:
        response = get_farcaster_verified_addresses(fid)
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 400
    
    return jsonify(response), 200
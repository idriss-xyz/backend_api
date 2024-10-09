import json
from datetime import datetime

import requests
from flask import Blueprint, jsonify, request

from cache.redis_fc import redis_fc
from cache.utils import cache_get_all_followers, cache_get_follower
from utils.farcaster import update_follower
from utils.graph_ql.fc_connected_addresses import get_farcaster_verified_addresses

farcaster_bp = Blueprint("fc", __name__)


@farcaster_bp.route("/get-connected-addresses", methods=["GET"])
def get_fc_connected_addresses():
    fc_name = request.args.get("name")

    if not fc_name:
        return jsonify({"error": "Missing name parameter"}), 400

    try:
        response = get_farcaster_verified_addresses(fc_name)
        socials = response.get("Socials", {}).get("Social", [])
        if not socials:
            return jsonify({"error": "No socials data found"}), 404
        addresses = socials[0].get("connectedAddresses", [])
        fid = socials[0].get("userId")
        if not fid:
            return jsonify({"error": "FID not found"}), 404
        freshest_evm_address = max(
            (addr for addr in addresses if addr.get("address", "").startswith("0x")),
            key=lambda addr: datetime.fromisoformat(addr["timestamp"].replace("Z", "+00:00")),
            default=None
        )
        if freshest_evm_address is None:
            return jsonify({"address": None, "fid": fid}), 200
        return jsonify({"address": freshest_evm_address["address"], "fid": fid}), 200
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400
    except (KeyError, TypeError) as e:
        return jsonify({"error": "Invalid response structure"}), 400


@farcaster_bp.route("/get-link", methods=["GET"])
def get_fc_link():
    """
    Endpoint to fetch follower (link) information for a given farcaster account name.
    """
    account = request.args.get("name")

    if not account:
        return jsonify({"error": "Missing name parameter"}), 400

    follower_data = cache_get_follower(account)

    try:
        return jsonify(follower_data), 200

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400
    

@farcaster_bp.route("/get-links", methods=["GET"])
def get_all_fc_links():
    """
    Endpoint to fetch followers information.
    """

    follower_data = cache_get_all_followers()

    try:
        return jsonify(follower_data), 200

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400
    

@farcaster_bp.route("/update-fc-follower", methods=["GET"])
def update_fc_follower():
    """
    Endpoint to update the followers of @idriss on farcaster.
    This endpoint will be called periodically to update the cache.
    """
    try:
        follower_data = update_follower()
        redis_fc.set("followers", json.dumps(follower_data), ex=600)

        return jsonify({"status": "Follower accounts updated", "accounts": follower_data}), 200

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400
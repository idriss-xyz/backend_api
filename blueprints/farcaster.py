from datetime import datetime

import requests
from flask import Blueprint, jsonify, request

from database.utils import get_all_follower, get_follower_with_connected_address
from server_responses.responses import HTTP_BAD_REQUEST, HTTP_OK
from utils.farcaster import get_farcaster_verified_addresses_from_api, get_fid

farcaster_bp = Blueprint("fc", __name__)


@farcaster_bp.route("/get-connected-addresses", methods=["GET"])
def get_fc_connected_addresses():
    fc_name = request.args.get("name")

    if not fc_name:
        return jsonify({"error": "Missing name parameter"}), HTTP_BAD_REQUEST

    try:
        response_fid = get_fid(fc_name)
        fid = response_fid.get("fid")
        print("fid", fid)
        if not fid:
            return jsonify({"error": "FID not found"}), HTTP_BAD_REQUEST
        primary_address = get_farcaster_verified_addresses_from_api(fid)
        print(primary_address)
        return (
            jsonify(
                {"address": primary_address["result"]["address"]["address"], "fid": fid}
            ),
            HTTP_OK,
        )
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid response structure"}), HTTP_BAD_REQUEST


@farcaster_bp.route("/get-link", methods=["GET"])
def get_fc_link():
    """
    Endpoint to fetch follower (link) information for a given farcaster account name.
    """
    account = request.args.get("name")

    if not account:
        return jsonify({"error": "Missing name parameter"}), HTTP_BAD_REQUEST

    follower_data = get_follower_with_connected_address(account)

    try:
        return jsonify(follower_data), HTTP_OK

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@farcaster_bp.route("/get-links", methods=["GET"])
def get_all_fc_links():
    """
    Endpoint to fetch followers information.
    """

    follower_data = get_follower_with_connected_address()

    try:
        return jsonify(follower_data), HTTP_OK

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST


@farcaster_bp.route("/get-all-followers", methods=["GET"])
def get_all_fc_followers():
    """
    Endpoint to fetch followers name and fid.
    """

    follower_data = get_all_follower()

    try:
        return jsonify(follower_data), HTTP_OK

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), HTTP_BAD_REQUEST

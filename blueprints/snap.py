import requests
from flask import Blueprint, jsonify, request

from limiter import limiter
from twitter import fetch_twitter_ids
from utils.farcaster import get_farcaster_verified_addresses_from_api
from utils.unstoppable_domains import get_unstoppable_domain_owner

snap_bp = Blueprint("resolver_snap", __name__)


@snap_bp.route("/get-twitter-id", methods=["GET"])
@limiter.limit("30 per minute")
def get_twitter():
    identifier = request.args.get("identifier").replace("@", "")

    if not identifier:
        return jsonify({"error": "Missing identifier parameter"}), 400

    try:
        response = fetch_twitter_ids(identifier)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400
    formatted_response = {"id": response["twitterIDs"].get(identifier, "Not found")}
    return jsonify(formatted_response), 200


@snap_bp.route("/snap/get-connected-addresses", methods=["GET"])
def get_fc_connected_address_for_snap():
    fid = request.args.get("fid")

    if not fid:
        return jsonify({"error": "Missing fid parameter"}), 400

    try:
        response = get_farcaster_verified_addresses_from_api(fid)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(response), 200


@snap_bp.route("/resolve-unstoppable-domains", methods=["GET"])
@limiter.limit("10 per minute")
def get_ud_for_snap():
    domain = request.args.get("domain")

    if not domain:
        return jsonify({"error": "Missing identifier parameter"}), 400

    try:
        response = get_unstoppable_domain_owner(domain)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 400
    return jsonify(response), 200

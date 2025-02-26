import os

from flask import Blueprint, make_response, render_template, request

from database.utils import add_creator_link, get_all_creator_links
from server_responses import HTTP_OK, create_response
from server_responses.responses import (
    HTTP_BAD_REQUEST,
    HTTP_FORBIDDEN_REQUEST,
    HTTP_UNAUTHORIZED_REQUEST,
)
from utils.helper import purge_links
from utils.validator import ALLOWED_ORIGINS, is_valid_donation_url
from web3_utils import ns

creators_bp = Blueprint("creators", __name__)


@creators_bp.route("/creators/links", methods=["POST"])
def add_creator_link_endpoint():
    origin = request.headers.get("Origin") or request.headers.get("Referer")
    if not origin or not any(origin.startswith(allowed) for allowed in ALLOWED_ORIGINS):
        return create_response({"error": "Forbidden"}, HTTP_FORBIDDEN_REQUEST)

    data = request.get_json()
    donation_url = data.get("donationURL") if data else None
    if (
        not donation_url
        or not isinstance(donation_url, str)
        or not is_valid_donation_url(donation_url)
    ):
        return create_response(
            {"error": "Invalid or missing donationURL"}, HTTP_BAD_REQUEST
        )

    result = add_creator_link(donation_url)
    if result == HTTP_OK:
        return create_response({"success": True}, HTTP_OK)
    return create_response({"error": "Failed to add link"}, HTTP_BAD_REQUEST)


@creators_bp.route("/creators/links", methods=["GET"])
def get_creator_links_endpoint():
    secret = request.args.get("secret")
    if secret != os.environ.get("CREATOR_LINKS_SECRET"):
        return create_response({"error": "Unauthorized"}, HTTP_UNAUTHORIZED_REQUEST)

    links = get_all_creator_links()
    unique_addresses = purge_links(links)
    if links is None:
        return create_response({"error": "Failed to fetch links"}, HTTP_BAD_REQUEST)

    unique_count = len(unique_addresses)
    return create_response({"count": unique_count, "links": links}, HTTP_OK)


@creators_bp.route("/v1/ENS-Addresses", methods=["GET"])
def find_address():
    try:
        args = request.args
        address_to_resolve = args["identifier"]
        reverse_resolved = ns.name(address_to_resolve)
        if address_to_resolve != ns.address(reverse_resolved):
            reverse_resolved = None
    except Exception:
        reverse_resolved = None
    response = create_response({"name": reverse_resolved}, HTTP_OK)
    return response


@creators_bp.route("/creators/obs", methods=["GET"])
def serve_obs():
    response = make_response(render_template("obs.html"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

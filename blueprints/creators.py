from flask import Blueprint, request

from server_responses import HTTP_OK, create_response
from web3_utils import ns

creators_bp = Blueprint("creators", __name__)


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

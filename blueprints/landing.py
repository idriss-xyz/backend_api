from email_validator import EmailNotValidError, validate_email
from flask import Blueprint, request

from database.utils import set_subscription
from limiter import limiter
from server_responses import HTTP_BAD_REQUEST, HTTP_OK, create_response
from utils.file_handler import get_eligibility

landing_bp = Blueprint("landing", __name__)


@landing_bp.route("/subscribe", methods=["POST", "OPTIONS"])
@limiter.limit("5 per minute")
def return_service_status():
    """
    Subscribes a user to upcoming prediction market news.

    Returns:
        Response: Subscription status
    """
    if request.method == "OPTIONS":
        return create_response("POST, OPTIONS")

    data = request.get_json()

    if not data or "email" not in data:
        return create_response({"error": "Email is required."}, HTTP_BAD_REQUEST)

    email = data["email"].strip()

    try:
        valid = validate_email(email)
        email = valid.email
    except EmailNotValidError as e:
        return create_response({"error": str(e)}, HTTP_BAD_REQUEST)
    status = set_subscription(email)
    return create_response({}, status)


@landing_bp.route("/check-eligibility/<address>", methods=["GET", "OPTIONS"])
@limiter.limit("5 per minute")
def return_eligibility(address):
    if request.method == "OPTIONS":
        return create_response("GET, OPTIONS")

    try:
        eligibility_status = get_eligibility(address.strip().lower())
    except EmailNotValidError as e:
        return create_response({"error": str(e)}, HTTP_BAD_REQUEST)
    return create_response(eligibility_status, HTTP_OK)

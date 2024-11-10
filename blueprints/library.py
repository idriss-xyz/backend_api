from flask import Blueprint, request

from server_responses import HTTP_OK, create_response
from twitter import fetch_twitter_ids, fetch_twitter_usernames

library_bp = Blueprint("library", __name__)


@library_bp.route("/v2/getTwitterNames", methods=["GET"])
def get_twitter_names():
    args_library = request.args
    result_names_cache_library = {}
    try:
        all_ids = args_library["ids"].split(",")
        result_names_library = fetch_twitter_usernames(all_ids)
        for user_id in all_ids:
            if not result_names_library.get(user_id, None):
                result_names_library[user_id] = None
    except Exception:
        result_names_library = result_names_cache_library
    response = create_response(result_names_library, HTTP_OK)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@library_bp.route("/v2/getTwitterID", methods=["GET"])
def get_twitter_id_library():
    args_library = request.args
    try:
        name = [args_library["identifier"].replace("@", "").lower()]
        result_ids_library = fetch_twitter_ids(name)
        twitter_id_library = result_ids_library[name]
    except Exception:
        twitter_id_library = "Not found"
    response = create_response({"twitterID": twitter_id_library}, HTTP_OK)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

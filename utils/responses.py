from flask import jsonify, make_response

HTTP_OK = 200
HTTP_BAD_REQUEST = 400
HTTP_NOT_FOUND = 404
HTTP_BAD_GATEWAY = 502

def create_response(data, status_code=HTTP_OK):
    """
    Creates a Flask response with the given data and status code.

    Args:
        data (dict or list): The response data.
        status_code (int): The HTTP status code.

    Returns:
        Response: The Flask response object.
    """
    json_data = jsonify(data)

    response = make_response(json_data, status_code)
    response.headers["Content-Type"] = "application/json"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

def handle_options_request(methods="GET, OPTIONS"):
    """
    Handles CORS preflight requests.

    Returns:
        Response: The Flask response object for OPTIONS requests.
    """
    response = make_response({"message": "ok"}, HTTP_OK)
    response.headers["Access-Control-Allow-Methods"] = methods
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response
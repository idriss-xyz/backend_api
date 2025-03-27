import os

from flask import Flask, jsonify
from flask_cors import CORS

from blueprints import (
    creators_bp,
    extension_bp,
    farcaster_bp,
    landing_bp,
    library_bp,
    snap_bp,
)
from cache import twitter_cache, twitter_name_cache
from limiter import limiter

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

limiter.init_app(app)
twitter_cache.init_app(app)
twitter_name_cache.init_app(app)

app.register_blueprint(creators_bp)
app.register_blueprint(snap_bp)
app.register_blueprint(farcaster_bp)
app.register_blueprint(extension_bp)
app.register_blueprint(landing_bp)
app.register_blueprint(library_bp)


@app.route("/")
def hello_world():
    return jsonify(message="Hello, API!")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get("PORT", 10000))

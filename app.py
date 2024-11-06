from flask import Flask, jsonify
from flask_cors import CORS

from blueprints import extension_bp, farcaster_bp, landing_bp, snap_bp
from utils.limiter import limiter

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

limiter.init_app(app)

app.register_blueprint(snap_bp)
app.register_blueprint(farcaster_bp)
app.register_blueprint(extension_bp)
app.register_blueprint(landing_bp)


@app.route("/")
def hello_world():
    return jsonify(message="Hello, API!")


if __name__ == "__main__":
    app.run(debug=True)

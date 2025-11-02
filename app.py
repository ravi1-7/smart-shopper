from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_file
from dealfinder import (
    get_location_details,
    get_google_shopping_deals,
    find_nearest_store_and_travel,
)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access


@app.route("/")
def index():
    return send_file("index.html")


@app.route("/api/search", methods=["POST"])
def search():
    data = request.json
    product = data.get("product")
    location = data.get("location")

    # Use your existing functions
    location_details = get_location_details(location)
    if not location_details:
        return jsonify([]), 200

    deals = get_google_shopping_deals(product, location_details["address"])

    for deal in deals:
        find_nearest_store_and_travel(
            deal,
            location_details["coords_str"],
            {"lat": location_details["lat"], "lng": location_details["lng"]},
        )

    # Convert deals to dict
    return jsonify([deal.__dict__ for deal in deals])


if __name__ == "__main__":
    app.run(port=5000, debug=True)

from flask import Flask, jsonify, request

from processor import process_search

app = Flask(__name__)


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field in request body"}), 400

    try:
        results = process_search(data)
        return jsonify({"status": "success", "results": results}), 200
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

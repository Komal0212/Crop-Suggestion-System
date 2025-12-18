from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/sensor", methods=["GET"])
def get_sensor():
    if os.path.exists(r"C:\Users\DELL\Desktop\crop recommendation\sensor.json"):
        with open(r"C:\Users\DELL\Desktop\crop recommendation\sensor.json") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "sensor.json not found"}), 404

@app.route("/prediction", methods=["GET"])
def get_pred():
    if os.path.exists(r"C:\Users\DELL\Desktop\crop recommendation\sensor.json"):
        with open(r"C:\Users\DELL\Desktop\crop recommendation\sensor.json") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "sensor.json not found"}), 404

@app.route("/graph", methods=["GET"])
def get_graph():
    if os.path.exists("trend.png"):
        return send_from_directory(".", "trend.png")
    else:
        return jsonify({"error": "trend.png not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

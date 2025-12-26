from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

@app.route("/check", methods=["POST"])
def check_license():
    data = request.json
    username = data.get("username", "").lower()

    users = load_users()

    if username not in users:
        return jsonify({"allowed": False})

    user = users[username]
    expiry = datetime.strptime(user["expiry"], "%Y-%m-%d")

    if user["status"] != "active":
        return jsonify({"allowed": False})

    if datetime.utcnow() > expiry:
        return jsonify({"allowed": False})

    return jsonify({"allowed": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

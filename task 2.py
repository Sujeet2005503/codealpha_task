from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_db, create_table
from encryption import encrypt_data
from capability import validate_capability

app = Flask(__name__)
CORS(app)   # ✅ THIS FIXES OPTIONS 404

create_table()

@app.route("/")
def home():
    return jsonify({"status": "Secure SQL Injection Project Running"})

@app.route("/register", methods=["POST"])
def register():
    token = request.headers.get("Capability-Code")
    if not validate_capability(token):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    username = encrypt_data(data["username"])
    password = encrypt_data(data["password"])

    db = get_db()
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )
    db.commit()
    db.close()

    return jsonify({"message": "User Registered Securely"})

if __name__ == "__main__":
    app.run(debug=True)


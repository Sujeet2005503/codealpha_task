from flask import Flask, request, jsonify
from db import get_db, create_table
from encryption import encrypt_data, decrypt_data
from capability import validate_capability

app = Flask(__name__)
create_table()

@app.route("/")
def home():
    return jsonify({"status": "Secure SQL Injection Project Running"})

# REGISTER USER (SECURE)
@app.route("/register", methods=["POST"])
def register():
    token = request.headers.get("Capability-Code")
    if not validate_capability(token):
        return jsonify({"error": "Unauthorized Access"}), 403

    data = request.json
    username = encrypt_data(data["username"])
    password = encrypt_data(data["password"])

    db = get_db()
    db.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)   # 🔐 SQL Injection SAFE
    )
    db.commit()
    db.close()

    return jsonify({"message": "User Registered Securely"})

# LOGIN (SQL INJECTION BLOCKED)
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = encrypt_data(data["username"])

    db = get_db()
    cur = db.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )
    user = cur.fetchone()
    db.close()

    if user:
        return jsonify({"status": "Login Successful"})
    else:
        return jsonify({"status": "Invalid Credentials"})

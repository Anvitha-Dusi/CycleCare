"""
routes/auth.py
-------------------------------------------------------------------------------
Handles user authentication: registration, login, logout, and session checks.
Demonstrates:
- Password hashing with Werkzeug
- Server-side input validation
- Session-based authentication
- Parameterized SQL queries to prevent SQL injection
-------------------------------------------------------------------------------
"""

import re
from functools import wraps
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import query_db, execute_db

auth_bp = Blueprint("auth", __name__)

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def login_required(f):
    """
    Decorator to protect routes requiring an authenticated user session.
    Returns HTTP 401 Unauthorized if the user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({
                "success": False,
                "message": "Authentication required. Please log in."
            }), 401
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route("/api/register", methods=["POST"])
def register():
    """
    POST /api/register
    Creates a new user account with hashed password.
    """
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    confirm_password = data.get("confirm_password") or ""

    # 1. Validation
    if not name:
        return jsonify({"success": False, "message": "Name is required."}), 400

    if not email or not re.match(EMAIL_REGEX, email):
        return jsonify({"success": False, "message": "A valid email address is required."}), 400

    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters long."}), 400

    if password != confirm_password:
        return jsonify({"success": False, "message": "Passwords do not match."}), 400

    # 2. Check if user already exists
    existing_user = query_db("SELECT id FROM users WHERE email = %s", (email,), one=True)
    if existing_user:
        return jsonify({"success": False, "message": "An account with this email already exists."}), 400

    # 3. Hash password and store user
    password_hash = generate_password_hash(password)
    user_id = execute_db(
        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
        (name, email, password_hash)
    )

    # Automatically establish session after successful registration
    session["user_id"] = user_id
    session["user_name"] = name
    session["user_email"] = email

    return jsonify({
        "success": True,
        "message": "Account created successfully!",
        "user": {
            "id": user_id,
            "name": name,
            "email": email
        }
    }), 201


@auth_bp.route("/api/login", methods=["POST"])
def login():
    """
    POST /api/login
    Authenticates a user via email and password.
    """
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"success": False, "message": "Both email and password are required."}), 400

    # Query user record
    user = query_db(
        "SELECT id, name, email, password_hash FROM users WHERE email = %s",
        (email,),
        one=True
    )

    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify({"success": False, "message": "Invalid email or password."}), 401

    # Store user identity in Flask session
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]

    return jsonify({
        "success": True,
        "message": f"Welcome back, {user['name']}!",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }), 200


@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    """
    POST /api/logout
    Clears the current session.
    """
    session.clear()
    return jsonify({
        "success": True,
        "message": "You have been logged out successfully."
    }), 200


@auth_bp.route("/api/me", methods=["GET"])
def get_current_user():
    """
    GET /api/me
    Returns current authenticated session user profile, or 401 if not logged in.
    """
    if "user_id" not in session:
        return jsonify({"success": False, "authenticated": False}), 401

    return jsonify({
        "success": True,
        "authenticated": True,
        "user": {
            "id": session["user_id"],
            "name": session.get("user_name"),
            "email": session.get("user_email")
        }
    }), 200

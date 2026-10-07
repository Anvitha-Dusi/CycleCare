"""
app.py
-------------------------------------------------------------------------------
Main application entry point for CycleCare.
Demonstrates:
- Flask application factory and modular blueprint registration
- Environment variable configuration
- Server-side routing for HTML views
- RESTful JSON API error handlers
- Database bootstrap on application startup
-------------------------------------------------------------------------------
"""

import os
from flask import Flask, render_template, jsonify, session, redirect, url_for
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

from database.db import init_db
from routes.auth import auth_bp
from routes.cycles import cycles_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "cyclecare_default_secret_key_2026")

# Register modular blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(cycles_bp)
app.register_blueprint(dashboard_bp)


# -----------------------------------------------------------------------------
# Frontend View Routes (HTML Page Delivery)
# -----------------------------------------------------------------------------

@app.route("/")
def index():
    """Serves the Landing page."""
    # If already logged in, convenient redirect to dashboard
    if "user_id" in session:
        return redirect(url_for("dashboard_view"))
    return render_template("index.html")


@app.route("/register")
def register_view():
    """Serves the Registration page."""
    if "user_id" in session:
        return redirect(url_for("dashboard_view"))
    return render_template("register.html")


@app.route("/login")
def login_view():
    """Serves the Login page."""
    if "user_id" in session:
        return redirect(url_for("dashboard_view"))
    return render_template("login.html")


@app.route("/dashboard")
def dashboard_view():
    """Serves the Dashboard page."""
    if "user_id" not in session:
        return redirect(url_for("login_view"))
    return render_template("dashboard.html", user_name=session.get("user_name", "User"))


@app.route("/history")
def history_view():
    """Serves the Cycle History page."""
    if "user_id" not in session:
        return redirect(url_for("login_view"))
    return render_template("history.html", user_name=session.get("user_name", "User"))


# -----------------------------------------------------------------------------
# Error Handlers
# -----------------------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"success": False, "message": "Resource or route not found."}), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"success": False, "message": "An unexpected server error occurred."}), 500


# -----------------------------------------------------------------------------
# Application Startup
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Initialize database tables on server start
    with app.app_context():
        init_db()

    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")
    print(f"\n[CycleCare] Application starting on http://localhost:{port}")
    print("[CycleCare] Menstrual Health & Cycle Tracking Web Application")
    print("[CycleCare] Ready for browser requests...\n")
    app.run(host="0.0.0.0", port=port, debug=debug)

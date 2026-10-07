"""
routes/dashboard.py
-------------------------------------------------------------------------------
Handles dashboard analytics and cycle estimation calculation:
- GET /api/dashboard

Demonstrates:
- Server-side data aggregation and statistical averages
- Cycle estimation business logic (Last Start Date + Average Cycle Length)
- Educational disclaimer integration
-------------------------------------------------------------------------------
"""

from datetime import datetime, date, timedelta
from flask import Blueprint, jsonify, session
from database.db import query_db
from routes.auth import login_required
from routes.cycles import format_cycle_row, parse_date

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/api/dashboard", methods=["GET"])
@login_required
def get_dashboard_data():
    """
    GET /api/dashboard
    Returns summary statistics, estimated next cycle date, and recent history.
    """
    user_id = session["user_id"]
    user_name = session.get("user_name", "User")

    # Fetch all cycles for user ordered chronologically descending
    cycles = query_db(
        "SELECT id, user_id, start_date, end_date, period_duration, cycle_length, notes, created_at "
        "FROM cycles WHERE user_id = %s ORDER BY start_date DESC",
        (user_id,)
    )

    total_cycles = len(cycles)
    today = date.today()

    if total_cycles == 0:
        return jsonify({
            "success": True,
            "user_name": user_name,
            "welcome_message": f"Welcome, {user_name}!",
            "has_data": False,
            "total_cycles": 0,
            "last_period": None,
            "avg_cycle_length": None,
            "avg_period_duration": None,
            "estimated_next_period": None,
            "days_until_next": None,
            "recent_cycles": [],
            "disclaimer": (
                "Educational Disclaimer: CycleCare predictions are mathematical estimations "
                "based on your historical averages and are NOT medical advice or diagnostic tools."
            )
        }), 200

    # Calculate averages
    cycle_lengths = [int(c["cycle_length"]) for c in cycles if c.get("cycle_length")]
    period_durations = [int(c["period_duration"]) for c in cycles if c.get("period_duration")]

    avg_cycle_length = round(sum(cycle_lengths) / len(cycle_lengths)) if cycle_lengths else 28
    avg_period_duration = round(sum(period_durations) / len(period_durations)) if period_durations else 5

    # Latest recorded cycle
    last_cycle = cycles[0]
    last_start = parse_date(str(last_cycle["start_date"]))

    # Cycle Estimation Calculation:
    # Estimated Next Period = Last Period Start Date + Average Cycle Length
    estimated_next_date = last_start + timedelta(days=avg_cycle_length)
    days_until_next = (estimated_next_date - today).days

    # Format recent cycles (top 5)
    recent_cycles = [format_cycle_row(c) for c in cycles[:5]]

    return jsonify({
        "success": True,
        "user_name": user_name,
        "welcome_message": f"Welcome back, {user_name}!",
        "has_data": True,
        "total_cycles": total_cycles,
        "last_period": format_cycle_row(last_cycle),
        "avg_cycle_length": avg_cycle_length,
        "avg_period_duration": avg_period_duration,
        "estimated_next_period": estimated_next_date.strftime("%Y-%m-%d"),
        "estimated_next_period_formatted": estimated_next_date.strftime("%B %d, %Y"),
        "days_until_next": days_until_next,
        "formula_explanation": (
            f"Estimated Next Period = Last Period Start Date ({last_start.strftime('%b %d, %Y')}) "
            f"+ Average Cycle Length ({avg_cycle_length} days) = {estimated_next_date.strftime('%b %d, %Y')}"
        ),
        "recent_cycles": recent_cycles,
        "all_cycles": [format_cycle_row(c) for c in cycles],
        "disclaimer": (
            "Educational Disclaimer: CycleCare predictions are mathematical estimations "
            "based on your recorded cycle history and are NOT medical advice or clinical diagnoses."
        )
    }), 200

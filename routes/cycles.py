"""
routes/cycles.py
-------------------------------------------------------------------------------
Handles full CRUD operations for menstrual cycle records:
- CREATE: POST /api/cycles
- READ (List): GET /api/cycles
- READ (Single): GET /api/cycles/<id>
- UPDATE: PUT /api/cycles/<id>
- DELETE: DELETE /api/cycles/<id>

Demonstrates:
- RESTful API principles (proper HTTP verbs and status codes)
- Authorization and user data isolation (WHERE user_id = session['user_id'])
- Input sanitization and date validation
- Parameterized SQL updates and deletions
-------------------------------------------------------------------------------
"""

from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session
from database.db import query_db, execute_db
from routes.auth import login_required

cycles_bp = Blueprint("cycles", __name__)


def parse_date(date_str):
    """Utility to parse YYYY-MM-DD string into date object."""
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def format_cycle_row(row):
    """Formats database row date objects into standard ISO strings for JSON."""
    if not row:
        return None
    d = dict(row)
    if d.get("start_date") and hasattr(d["start_date"], "strftime"):
        d["start_date"] = d["start_date"].strftime("%Y-%m-%d")
    elif d.get("start_date"):
        d["start_date"] = str(d["start_date"])

    if d.get("end_date") and hasattr(d["end_date"], "strftime"):
        d["end_date"] = d["end_date"].strftime("%Y-%m-%d")
    elif d.get("end_date"):
        d["end_date"] = str(d["end_date"])

    if d.get("created_at") and hasattr(d["created_at"], "strftime"):
        d["created_at"] = d["created_at"].strftime("%Y-%m-%d %H:%M:%S")
    elif d.get("created_at"):
        d["created_at"] = str(d["created_at"])
    return d


@cycles_bp.route("/api/cycles", methods=["GET"])
@login_required
def get_cycles():
    """
    GET /api/cycles
    Retrieves all cycle records belonging strictly to the logged-in user.
    """
    user_id = session["user_id"]
    rows = query_db(
        "SELECT id, user_id, start_date, end_date, period_duration, cycle_length, notes, created_at "
        "FROM cycles WHERE user_id = %s ORDER BY start_date DESC",
        (user_id,)
    )
    formatted = [format_cycle_row(r) for r in rows]
    return jsonify({
        "success": True,
        "count": len(formatted),
        "cycles": formatted
    }), 200


@cycles_bp.route("/api/cycles/<int:cycle_id>", methods=["GET"])
@login_required
def get_cycle(cycle_id):
    """
    GET /api/cycles/<id>
    Retrieves a single cycle record by ID, verifying user ownership.
    """
    user_id = session["user_id"]
    record = query_db(
        "SELECT id, user_id, start_date, end_date, period_duration, cycle_length, notes, created_at "
        "FROM cycles WHERE id = %s",
        (cycle_id,),
        one=True
    )

    if not record:
        return jsonify({"success": False, "message": "Cycle record not found."}), 404

    # Authorization verification
    if record["user_id"] != user_id:
        return jsonify({"success": False, "message": "Unauthorized access to this cycle record."}), 403

    return jsonify({
        "success": True,
        "cycle": format_cycle_row(record)
    }), 200


@cycles_bp.route("/api/cycles", methods=["POST"])
@login_required
def create_cycle():
    """
    POST /api/cycles
    Creates a new cycle record for the logged-in user.
    """
    user_id = session["user_id"]
    data = request.get_json() or {}

    start_date_raw = data.get("start_date")
    end_date_raw = data.get("end_date")
    duration_raw = data.get("period_duration")
    cycle_length_raw = data.get("cycle_length")
    notes = (data.get("notes") or "").strip()

    # 1. Start date validation
    if not start_date_raw:
        return jsonify({"success": False, "message": "Period start date is required."}), 400

    start_date = parse_date(start_date_raw)
    if not start_date:
        return jsonify({"success": False, "message": "Invalid start date format. Please use YYYY-MM-DD."}), 400

    # 2. End date & duration validation
    end_date = None
    if end_date_raw and end_date_raw.strip():
        end_date = parse_date(end_date_raw)
        if not end_date:
            return jsonify({"success": False, "message": "Invalid end date format. Please use YYYY-MM-DD."}), 400
        if end_date < start_date:
            return jsonify({"success": False, "message": "End date cannot be earlier than start date."}), 400

    # Calculate or validate period duration
    period_duration = None
    if duration_raw is not None and str(duration_raw).strip() != "":
        try:
            period_duration = int(duration_raw)
        except ValueError:
            return jsonify({"success": False, "message": "Period duration must be a valid number of days."}), 400
    elif end_date:
        # Calculate duration based on inclusive dates
        period_duration = (end_date - start_date).days + 1
    else:
        # Default reasonable period duration if neither provided
        period_duration = 5

    if period_duration < 1 or period_duration > 30:
        return jsonify({"success": False, "message": "Period duration must be between 1 and 30 days."}), 400

    # If end_date was not given, we can auto-fill it from period duration
    if not end_date:
        end_date = start_date + timedelta(days=period_duration - 1)

    # 3. Cycle length validation
    cycle_length = 28
    if cycle_length_raw is not None and str(cycle_length_raw).strip() != "":
        try:
            cycle_length = int(cycle_length_raw)
        except ValueError:
            return jsonify({"success": False, "message": "Cycle length must be a valid number of days."}), 400
    else:
        # Automatically calculate cycle length from the user's previous recorded cycle if available
        last_cycle = query_db(
            "SELECT start_date FROM cycles WHERE user_id = %s AND start_date < %s ORDER BY start_date DESC LIMIT 1",
            (user_id, start_date.strftime("%Y-%m-%d")),
            one=True
        )
        if last_cycle:
            last_date = parse_date(str(last_cycle["start_date"]))
            diff = (start_date - last_date).days
            if 15 <= diff <= 90:
                cycle_length = diff

    if cycle_length < 15 or cycle_length > 90:
        return jsonify({"success": False, "message": "Cycle length must be between 15 and 90 days."}), 400

    # 4. Insert into database
    new_id = execute_db(
        "INSERT INTO cycles (user_id, start_date, end_date, period_duration, cycle_length, notes) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (
            user_id,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d") if end_date else None,
            period_duration,
            cycle_length,
            notes if notes else None
        )
    )

    created_record = query_db("SELECT * FROM cycles WHERE id = %s", (new_id,), one=True)

    return jsonify({
        "success": True,
        "message": "Menstrual cycle record added successfully!",
        "cycle": format_cycle_row(created_record)
    }), 201


@cycles_bp.route("/api/cycles/<int:cycle_id>", methods=["PUT"])
@login_required
def update_cycle(cycle_id):
    """
    PUT /api/cycles/<id>
    Updates an existing cycle record for the logged-in user.
    """
    user_id = session["user_id"]
    existing = query_db("SELECT id, user_id FROM cycles WHERE id = %s", (cycle_id,), one=True)

    if not existing:
        return jsonify({"success": False, "message": "Cycle record not found."}), 404

    if existing["user_id"] != user_id:
        return jsonify({"success": False, "message": "Unauthorized to update this cycle record."}), 403

    data = request.get_json() or {}
    start_date_raw = data.get("start_date")
    end_date_raw = data.get("end_date")
    duration_raw = data.get("period_duration")
    cycle_length_raw = data.get("cycle_length")
    notes = (data.get("notes") or "").strip()

    if not start_date_raw:
        return jsonify({"success": False, "message": "Period start date is required."}), 400

    start_date = parse_date(start_date_raw)
    if not start_date:
        return jsonify({"success": False, "message": "Invalid start date format. Please use YYYY-MM-DD."}), 400

    end_date = None
    if end_date_raw and end_date_raw.strip():
        end_date = parse_date(end_date_raw)
        if not end_date:
            return jsonify({"success": False, "message": "Invalid end date format. Please use YYYY-MM-DD."}), 400
        if end_date < start_date:
            return jsonify({"success": False, "message": "End date cannot be earlier than start date."}), 400

    # Period duration
    try:
        period_duration = int(duration_raw) if duration_raw else ((end_date - start_date).days + 1 if end_date else 5)
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid period duration."}), 400

    if period_duration < 1 or period_duration > 30:
        return jsonify({"success": False, "message": "Period duration must be between 1 and 30 days."}), 400

    if not end_date:
        end_date = start_date + timedelta(days=period_duration - 1)

    # Cycle length
    try:
        cycle_length = int(cycle_length_raw) if cycle_length_raw else 28
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid cycle length."}), 400

    if cycle_length < 15 or cycle_length > 90:
        return jsonify({"success": False, "message": "Cycle length must be between 15 and 90 days."}), 400

    # Execute parameterized update
    execute_db(
        "UPDATE cycles SET start_date = %s, end_date = %s, period_duration = %s, cycle_length = %s, notes = %s "
        "WHERE id = %s AND user_id = %s",
        (
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            period_duration,
            cycle_length,
            notes if notes else None,
            cycle_id,
            user_id
        )
    )

    updated_record = query_db("SELECT * FROM cycles WHERE id = %s", (cycle_id,), one=True)

    return jsonify({
        "success": True,
        "message": "Cycle record updated successfully!",
        "cycle": format_cycle_row(updated_record)
    }), 200


@cycles_bp.route("/api/cycles/<int:cycle_id>", methods=["DELETE"])
@login_required
def delete_cycle(cycle_id):
    """
    DELETE /api/cycles/<id>
    Deletes an existing cycle record belonging to the logged-in user.
    """
    user_id = session["user_id"]
    existing = query_db("SELECT id, user_id FROM cycles WHERE id = %s", (cycle_id,), one=True)

    if not existing:
        return jsonify({"success": False, "message": "Cycle record not found."}), 404

    if existing["user_id"] != user_id:
        return jsonify({"success": False, "message": "Unauthorized to delete this cycle record."}), 403

    execute_db("DELETE FROM cycles WHERE id = %s AND user_id = %s", (cycle_id, user_id))

    return jsonify({
        "success": True,
        "message": "Cycle record deleted successfully!"
    }), 200

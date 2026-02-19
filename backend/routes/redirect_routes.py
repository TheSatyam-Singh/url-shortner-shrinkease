from flask import Blueprint, request, redirect, jsonify
from datetime import datetime
import sqlite3

redirect_bp = Blueprint("redirect", __name__)


def get_db():
    # import here to avoid circular import when blueprint is loaded by app
    from app import get_db as _get_db

    return _get_db()


@redirect_bp.route("/<short_code>", methods=["GET"])
def handle_redirect(short_code):
    db = get_db()

    try:
        row = db.execute(
            "SELECT id, original_url FROM urls WHERE short_code = ?",
            (short_code,),
        ).fetchone()
    except sqlite3.Error:
        return jsonify({"error": "Database connection failed"}), 503

    if not row:
        return jsonify({"error": "Short URL not found"}), 404

    # increment clicks
    try:
        db.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE id = ?",
            (row["id"],),
        )
        db.commit()
    except sqlite3.Error:
        # non-fatal for redirect — still redirect even if counter failed
        pass

    original = row["original_url"]

    # Ensure URL has a scheme (should already be normalized on insert)
    if not original.startswith(("http://", "https://")):
        original = "https://" + original

    return redirect(original, code=302)

from flask import Blueprint, redirect
import sqlite3

redirect_bp = Blueprint("redirect", __name__)


@redirect_bp.route("/<short_code>")
def redirect_url(short_code):
    from app import get_db

    db = get_db()

    try:
        row = db.execute(
            "SELECT id, original_url FROM urls WHERE short_code = ?",
            (short_code,),
        )
        url_doc = row.fetchone()
    except sqlite3.Error:
        return "Database connection failed", 503

    if not url_doc:
        return "URL not found", 404

    try:
        db.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE id = ?",
            (url_doc["id"],),
        )
        db.commit()
    except sqlite3.Error:
        return "Database connection failed", 503

    return redirect(url_doc["original_url"])

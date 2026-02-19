import string
import random
import io
import base64
import sqlite3
from datetime import datetime, timezone

import qrcode
from flask import Blueprint, request, jsonify
from config import BASE_URL

url_bp = Blueprint("url", __name__)


def get_public_base_url():
    if BASE_URL and BASE_URL.strip():
        return BASE_URL.rstrip("/")
    return request.url_root.rstrip("/")


def get_urls_collection():
    from app import get_db

    return get_db()


def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def make_qr_base64(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


@url_bp.route("/shorten", methods=["POST"])
def shorten_url():
    db = get_urls_collection()

    data = request.get_json()
    original_url = data.get("url", "").strip() if data else ""
    custom_code = data.get("custom_code", "").strip() if data else ""

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    if not original_url.startswith(("http://", "https://")):
        original_url = "https://" + original_url

    try:
        if custom_code:
            existing = db.execute(
                "SELECT id FROM urls WHERE short_code = ?",
                (custom_code,),
            ).fetchone()
            if existing:
                return jsonify({"error": "Custom code already taken"}), 409
            short_code = custom_code
        else:
            short_code = generate_short_code()
            while db.execute(
                "SELECT id FROM urls WHERE short_code = ?",
                (short_code,),
            ).fetchone():
                short_code = generate_short_code()
    except sqlite3.Error:
        return jsonify({"error": "Database connection failed"}), 503

    public_base_url = get_public_base_url()
    short_url = f"{public_base_url}/{short_code}"
    qr_data = make_qr_base64(short_url)

    try:
        db.execute(
            """
            INSERT INTO urls (original_url, short_code, clicks, created_at, qr_code)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                original_url,
                short_code,
                0,
                datetime.now(timezone.utc).isoformat(),
                qr_data,
            ),
        )
        db.commit()
    except sqlite3.Error:
        return jsonify({"error": "Database connection failed"}), 503

    return jsonify(
        {
            "short_url": short_url,
            "short_code": short_code,
            "original_url": original_url,
            "qr_code": qr_data,
        }
    ), 201


@url_bp.route("/urls", methods=["GET"])
def get_user_urls():
    db = get_urls_collection()

    try:
        urls = db.execute(
            "SELECT id, original_url, short_code, clicks, created_at, qr_code FROM urls ORDER BY id DESC"
        ).fetchall()
    except sqlite3.Error:
        return jsonify({"error": "Database connection failed"}), 503

    result = []
    for row in urls:
        result.append(
            {
                "id": str(row["id"]),
                "original_url": row["original_url"],
                "short_code": row["short_code"],
                "short_url": f"{get_public_base_url()}/{row['short_code']}",
                "clicks": row["clicks"],
                "created_at": row["created_at"],
                "qr_code": row["qr_code"] or "",
            }
        )
    return jsonify(result), 200


@url_bp.route("/urls/<url_id>", methods=["DELETE"])
def delete_url(url_id):
    db = get_urls_collection()

    if not url_id.isdigit():
        return jsonify({"error": "Invalid URL id"}), 400

    try:
        cursor = db.execute(
            "DELETE FROM urls WHERE id = ?",
            (int(url_id),),
        )
        db.commit()
    except sqlite3.Error:
        return jsonify({"error": "Database connection failed"}), 503

    if cursor.rowcount == 0:
        return jsonify({"error": "URL not found"}), 404
    return jsonify({"message": "Deleted"}), 200


@url_bp.route("/urls/<url_id>/stats", methods=["GET"])
def url_stats(url_id):
    db = get_urls_collection()

    if not url_id.isdigit():
        return jsonify({"error": "Invalid URL id"}), 400

    try:
        row = db.execute(
            "SELECT id, original_url, short_code, clicks, created_at FROM urls WHERE id = ?",
            (int(url_id),),
        )
        url_doc = row.fetchone()
    except sqlite3.Error:
        return jsonify({"error": "Database connection failed"}), 503

    if not url_doc:
        return jsonify({"error": "URL not found"}), 404

    return jsonify(
        {
            "id": str(url_doc["id"]),
            "original_url": url_doc["original_url"],
            "short_code": url_doc["short_code"],
            "short_url": f"{get_public_base_url()}/{url_doc['short_code']}",
            "clicks": url_doc["clicks"],
            "created_at": url_doc["created_at"],
        }
    ), 200

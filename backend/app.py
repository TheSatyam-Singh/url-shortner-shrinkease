import os
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS
from flask import g
from werkzeug.middleware.proxy_fix import ProxyFix
from config import SECRET_KEY, CORS_ALLOWED_ORIGINS, DB_PATH

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

CORS(
    app,
    resources={r"/*": {"origins": CORS_ALLOWED_ORIGINS}},
    supports_credentials=False,
    allow_headers=["Content-Type", "Authorization"],
    methods=["GET", "HEAD", "POST", "OPTIONS", "PUT", "DELETE"],
)

print(f"Configured CORS_ALLOWED_ORIGINS={CORS_ALLOWED_ORIGINS}")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE,
            clicks INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL,
            qr_code TEXT
        )
        """
    )
    db.commit()


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


with app.app_context():
    init_db()

from routes.url_routes import url_bp
from routes.redirect_routes import redirect_bp

app.register_blueprint(url_bp, url_prefix="/api")
app.register_blueprint(redirect_bp)

@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "service": "Flask API",
        "version": "1.0.0"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 4000)),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )

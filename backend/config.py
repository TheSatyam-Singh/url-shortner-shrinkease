import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
BASE_URL = os.getenv("BASE_URL", "").strip()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.getenv("DB_PATH", os.path.join(BASE_DIR, "urlshortner.db"))

CORS_ALLOWED_ORIGINS_RAW = os.getenv("CORS_ALLOWED_ORIGINS", "*")
if CORS_ALLOWED_ORIGINS_RAW.strip() == "*":
    CORS_ALLOWED_ORIGINS = "*"
else:
    CORS_ALLOWED_ORIGINS = [
        origin.strip()
        for origin in CORS_ALLOWED_ORIGINS_RAW.split(",")
        if origin.strip()
    ]

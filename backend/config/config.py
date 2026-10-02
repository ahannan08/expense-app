import os
from pathlib import Path

from dotenv import load_dotenv

_backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(_backend_dir / ".env")

_DEFAULT_DB = "postgresql://postgres:postgres@localhost:5432/expense_app"


def _normalize_database_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql://", 1)
    return url


_raw_url = os.environ.get("DATABASE_URL", _DEFAULT_DB)
SQLALCHEMY_DATABASE_URI = _normalize_database_url(_raw_url)
SQLALCHEMY_TRACK_MODIFICATIONS = False

FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")

BACKEND_ROOT = _backend_dir

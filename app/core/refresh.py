import secrets
from datetime import datetime, timedelta

from app.config import settings


def generate_refresh_token():
    return secrets.token_urlsafe(64)


def get_refresh_expiry():
    return datetime.utcnow() + timedelta(
        days=settings.refresh_token_expire_days
    )
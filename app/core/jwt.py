from datetime import datetime, timedelta
from jose import jwt

from app.config import settings
from app.core.key_store import KEYS, ACTIVE_KID


def create_access_token(data: dict):
    payload = data.copy()

    payload.update({
        "iss": settings.app_name,
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        ),
    })

    headers = {
        "kid": ACTIVE_KID
    }

    return jwt.encode(
        payload,
        KEYS[ACTIVE_KID]["private"],
        algorithm="RS256",
        headers=headers,
    )

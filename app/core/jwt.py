from datetime import datetime, timedelta
from jose import jwt

from app.core.keys import PRIVATE_KEY
from app.config import settings


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    to_encode.update({
        "exp": expire,
        "iss": settings.app_name
    })

    return jwt.encode(
        to_encode,
        PRIVATE_KEY,
        algorithm="RS256"
    )

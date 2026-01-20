from datetime import datetime, timedelta
from jose import jwt

from app.config import settings


def create_id_token(user_id: str, email: str, audience: str):
    payload = {
        "iss": settings.app_name,
        "sub": user_id,
        "aud": audience,
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=15),
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm,
    )

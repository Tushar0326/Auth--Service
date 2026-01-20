from fastapi import APIRouter
from app.config import settings

router = APIRouter()


@router.get("/.well-known/openid-configuration")
def openid_config():
    return {
        "issuer": settings.app_name,
        "authorization_endpoint": "/oauth/authorize",
        "token_endpoint": "/oauth/token",
        "userinfo_endpoint": "/oauth/userinfo",
        "scopes_supported": ["openid", "email", "profile"],
        "response_types_supported": ["code"],
        "grant_types_supported": ["authorization_code"],
        "id_token_signing_alg_values_supported": [settings.algorithm],
    }

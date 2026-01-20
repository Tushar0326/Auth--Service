from fastapi import APIRouter
from jose.utils import base64url_encode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from app.core.keys import PUBLIC_KEY

router = APIRouter()


@router.get("/.well-known/jwks.json")
def jwks():
    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY.encode(),
        backend=default_backend()
    )

    numbers = public_key.public_numbers()

    return {
        "keys": [
            {
                "kty": "RSA",
                "use": "sig",
                "alg": "RS256",
                "kid": "auth-key-1",
                "n": base64url_encode(numbers.n.to_bytes(256, "big")).decode(),
                "e": base64url_encode(numbers.e.to_bytes(3, "big")).decode(),
            }
        ]
    }

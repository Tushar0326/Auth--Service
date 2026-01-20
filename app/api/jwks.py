from fastapi import APIRouter
from jose.utils import base64url_encode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

from app.core.key_store import KEYS

router = APIRouter()


@router.get("/.well-known/jwks.json")
def jwks():
    jwk_keys = []

    for kid, keypair in KEYS.items():
        public_key = serialization.load_pem_public_key(
            keypair["public"].encode(),
            backend=default_backend()
        )

        numbers = public_key.public_numbers()

        jwk_keys.append({
            "kty": "RSA",
            "use": "sig",
            "alg": "RS256",
            "kid": kid,
            "n": base64url_encode(numbers.n.to_bytes(256, "big")).decode(),
            "e": base64url_encode(numbers.e.to_bytes(3, "big")).decode(),
        })

    return {"keys": jwk_keys}


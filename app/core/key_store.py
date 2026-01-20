from pathlib import Path
from jose import jwt

KEYS_DIR = Path("app/keys")

# active signing key
ACTIVE_KID = "key1"

KEYS = {
    "key1": {
        "private": (KEYS_DIR / "key1_private.pem").read_text(),
        "public": (KEYS_DIR / "key1_public.pem").read_text(),
    },
    # future key (for rotation)
    # "key2": {
    #     "private": (KEYS_DIR / "key2_private.pem").read_text(),
    #     "public": (KEYS_DIR / "key2_public.pem").read_text(),
    # },
}

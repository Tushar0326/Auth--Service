from pathlib import Path

PRIVATE_KEY_PATH = Path("app/keys/key1_private.pem")
PUBLIC_KEY_PATH = Path("app/keys/key1_public.pem")

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()

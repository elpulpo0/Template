# flake8: noqa: E402
import base64
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

secret_bytes = os.urandom(32)
secret_key = base64.urlsafe_b64encode(secret_bytes).rstrip(b"=").decode("utf-8")

print(f"Your generated secret key : {secret_key}")

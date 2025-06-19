import base64
import os
import sys
from pathlib import Path

# Ajouter la racine du projet dans sys.path pour que l'import fonctionne
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.utils.logger_config import configure_logger

logger = configure_logger()

secret_bytes = os.urandom(32)
secret_key = base64.urlsafe_b64encode(secret_bytes).rstrip(b'=').decode('utf-8')

logger.info(f"Your generated secret key : {secret_key}")

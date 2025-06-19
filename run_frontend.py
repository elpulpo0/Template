import os
from dotenv import load_dotenv
import subprocess
from backend.utils.logger_config import configure_logger

# Configuration du logger
logger = configure_logger()

# 1. Charger les variables d'environnement à la racine
load_dotenv()

PORT_BACK = os.getenv("PORT_BACK")
GITHUB_URL = os.getenv("GITHUB_URL")
APP_NAME = os.getenv("APP_NAME")
PORT_FRONT = os.getenv("PORT_FRONT")
frontend_env_path = os.path.join("frontend", ".env")

# 2. Créer / écraser frontend/.env
with open(frontend_env_path, "w") as f:
    f.write(f"VITE_PORT={PORT_FRONT}\n")
    f.write(f"VITE_PORT_BACK={PORT_BACK}\n")
    f.write(f"VITE_GITHUB_URL={GITHUB_URL}\n")
    f.write(f"VITE_APP_NAME={APP_NAME}\n")

logger.info(f"✅ Fichier '{frontend_env_path}' généré avec succès avec les valeurs : "
            f"VITE_PORT={PORT_FRONT}, VITE_PORT_BACK={PORT_BACK}, VITE_GITHUB_URL={GITHUB_URL}, VITE_APP_NAME={APP_NAME}")

# 3. Lancer npm run dev depuis frontend
try:
    subprocess.run("npm run dev", cwd="frontend", shell=True, check=True)
except subprocess.CalledProcessError as e:
    logger.error(f"❌ Erreur lors du lancement de npm : {e}")

import os
from dotenv import load_dotenv
import subprocess
from auth.utils.logger_config import configure_logger

logger = configure_logger()

load_dotenv()

PORT_AUTH = os.getenv("PORT_AUTH")
PORT_BACK = os.getenv("PORT_BACK")
GITHUB_URL = os.getenv("GITHUB_URL")
APP_NAME = os.getenv("APP_NAME")
PORT_FRONT = os.getenv("PORT_FRONT")
frontend_env_path = os.path.join("frontend", ".env")

with open(frontend_env_path, "w") as f:
    f.write(f"VITE_PORT={PORT_FRONT}\n")
    f.write(f"VITE_PORT_AUTH={PORT_AUTH}\n")
    f.write(f"VITE_PORT_BACK={PORT_BACK}\n")
    f.write(f"VITE_GITHUB_URL={GITHUB_URL}\n")
    f.write(f"VITE_APP_NAME={APP_NAME}\n")

logger.info(
    f"✅ File '{frontend_env_path}' successfully generated with values: "
    f"VITE_PORT={PORT_FRONT} "
    f"VITE_PORT_BACK={PORT_BACK} "
    f"VITE_PORT_AUTH={PORT_AUTH} "
    f"VITE_GITHUB_URL={GITHUB_URL} "
    f"VITE_APP_NAME={APP_NAME}"
)

try:
    subprocess.run("npm run dev", cwd="frontend", shell=True, check=True)
except subprocess.CalledProcessError as e:
    logger.error(f"❌ Error running npm: {e}")

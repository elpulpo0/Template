import os
import sys
import uvicorn
from dotenv import load_dotenv

backend_path = os.path.join(os.path.dirname(__file__), "backend")
os.chdir(backend_path)
sys.path.insert(0, backend_path)

from modules.api.users.create_db import init_users_db
from modules.api.main import create_app

load_dotenv()

PORT_BACK = int(os.getenv("PORT_BACK"))

if __name__ == "__main__":
    if os.getenv("RUN_ENV") != "test":
        init_users_db()
    uvicorn.run("backend.modules.api.main:app", host="0.0.0.0", port=PORT_BACK, reload=True)


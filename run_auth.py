# flake8: noqa: E402
import os
import sys
import uvicorn
from dotenv import load_dotenv

auth_path = os.path.join(os.path.dirname(__file__), "auth")
os.chdir(auth_path)
sys.path.insert(0, auth_path)

from auth.modules.api.users.create_db import init_users_db

load_dotenv()

PORT_AUTH = int(os.getenv("PORT_AUTH"))

if __name__ == "__main__":
    if os.getenv("RUN_ENV") != "test":
        init_users_db()
    uvicorn.run("auth.modules.api.main:app", host="0.0.0.0", port=PORT_AUTH, reload=True)

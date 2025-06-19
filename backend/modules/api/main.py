from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from modules.api.users.routes import users_router
from modules.api.auth.routes import auth_router

import os
from dotenv import load_dotenv

load_dotenv()
PORT_FRONT = os.getenv("PORT_FRONT", "5173")  # attention, chaîne !
FRONTEND_URL = os.getenv("FRONTEND_URL", f"http://localhost:{PORT_FRONT}")

def create_app() -> FastAPI:
    app = FastAPI(
    title="Template API",
    description="Template",
    version="1.0.0"
    )

    # Ajout du middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            FRONTEND_URL
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    router = APIRouter()
    router.include_router(auth_router, prefix="/auth", tags=["Authentification"])
    router.include_router(users_router, prefix="/users", tags=["Users"])

    app.include_router(router)

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    return app

app = create_app()
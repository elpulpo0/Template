from modules.api.auth.security import verify_password, anonymize, hash_token
from datetime import datetime, timedelta
from jose import jwt
import os
from dotenv import load_dotenv
from utils.logger_config import configure_logger
from modules.api.users.functions import get_user_by_email
from sqlalchemy.orm import Session
from modules.api.auth.models import RefreshToken


logger = configure_logger()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (
        expires_delta if expires_delta else timedelta(minutes=60)
    )

    role = data.get("role")
    scopes_map = {"admin": ["admin"], "reader": ["reader"]}
    scopes = scopes_map.get(role, [])

    token_type = data.get("type", "access")
    to_encode["token_type"] = token_type

    if token_type == "access":
        to_encode["scopes"] = scopes

    to_encode["exp"] = expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    if token_type == "access":
        logger.info(f"Token {token_type} créé (role: {role}) – Expiration : {expire.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        logger.info(f"Token {token_type} créé – Expiration : {expire.strftime('%Y-%m-%d %H:%M:%S')}")

    return encoded_jwt


def authenticate_user(db: Session, email: str, password: str):
    """Authentifie un utilisateur en vérifiant son email et son mot de passe."""

    anonymized_email = anonymize(email)  # Hacher l'email

    user = get_user_by_email(anonymized_email, db)

    if not user:
        logger.info("Utilisateur non trouvé.")
        return False

    if not verify_password(password, user.password):
        logger.info("Mot de passe invalide.")
        return False

    logger.info(f"{user.name.upper()} authentifié avec succès")
    return user


def store_refresh_token(db: Session, user_id: int, token: str, expires_at: datetime):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.revoked == False
    ).update({RefreshToken.revoked: True}, synchronize_session=False)

    refresh_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at,
    )
    db.add(refresh_token)
    db.commit()


def find_refresh_token(db: Session, provided_token: str) -> RefreshToken | None:
    refresh_token = (
        db.query(RefreshToken).filter(RefreshToken.token == provided_token).first()
    )
    if refresh_token:
        logger.info(
            f"""
            Refresh token found: {refresh_token.token},
            expires_at: {refresh_token.expires_at}
            """
        )
    else:
        logger.warning("No refresh token found.")
    return refresh_token


def verify_token(provided_token: str, stored_hash: str) -> bool:
    return hash_token(provided_token) == stored_hash

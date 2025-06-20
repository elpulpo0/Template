from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import USERS_DATABASE_URL

UsersBase = declarative_base()


def create_session(database_url: str):
    engine = create_engine(database_url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


users_engine, UsersSessionLocal = create_session(USERS_DATABASE_URL)

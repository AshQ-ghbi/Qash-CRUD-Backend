"""Database engine, session factory and FastAPI dependency (backend: app/database.py)."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite with FastAPI threads
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yield a database session and always close it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

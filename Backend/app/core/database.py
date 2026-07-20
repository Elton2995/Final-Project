from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import logging

from app.config import settings

logger = logging.getLogger(__name__)

# Create engine with settings from config
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=settings.DATABASE_POOL_PRE_PING if hasattr(settings, 'DATABASE_POOL_PRE_PING') else True,
    pool_recycle=settings.DATABASE_POOL_RECYCLE if hasattr(settings, 'DATABASE_POOL_RECYCLE') else 3600,
    pool_size=settings.DATABASE_POOL_SIZE if hasattr(settings, 'DATABASE_POOL_SIZE') else 10,
    max_overflow=settings.DATABASE_MAX_OVERFLOW if hasattr(settings, 'DATABASE_MAX_OVERFLOW') else 20,
    pool_timeout=settings.DATABASE_POOL_TIMEOUT if hasattr(settings, 'DATABASE_POOL_TIMEOUT') else 30,
    echo=settings.DATABASE_ECHO if hasattr(settings, 'DATABASE_ECHO') else False,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
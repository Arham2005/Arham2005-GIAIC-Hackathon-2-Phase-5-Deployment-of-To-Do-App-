from sqlmodel import SQLModel
from sqlalchemy import create_engine
from shared.core.config import settings
from shared.models.user import User  # Import models to register them
from shared.models.task import Task


def get_engine():
    """Create and return database engine"""
    engine = create_engine(settings.DATABASE_URL, echo=True)
    return engine


engine = get_engine()


def create_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(bind=engine)
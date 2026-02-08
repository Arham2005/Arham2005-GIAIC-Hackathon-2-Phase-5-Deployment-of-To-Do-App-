from sqlmodel import create_engine, Session, SQLModel
from shared.models.user import User
from shared.models.task import Task
from shared.core.settings import settings
import os

# Use the same database configuration as the main app
DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=False)

def create_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session"""
    with Session(engine) as session:
        yield session
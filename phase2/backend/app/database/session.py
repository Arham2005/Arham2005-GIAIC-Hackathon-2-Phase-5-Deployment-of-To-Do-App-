from sqlmodel import create_engine
from shared.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL, echo=True)
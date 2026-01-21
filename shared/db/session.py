from sqlmodel import create_engine
from shared.core.config import settings
from sqlalchemy.orm import sessionmaker


# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Set to False in production
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Dependency to get database session"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
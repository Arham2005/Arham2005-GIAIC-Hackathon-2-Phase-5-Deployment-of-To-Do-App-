from sqlmodel import create_engine
from shared.core.config import settings
from sqlalchemy.orm import sessionmaker


# Create engine with conditional connect_args
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite-specific connect_args
    connect_args = {"check_same_thread": False}
else:
    # PostgreSQL and other databases don't need this
    connect_args = {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
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
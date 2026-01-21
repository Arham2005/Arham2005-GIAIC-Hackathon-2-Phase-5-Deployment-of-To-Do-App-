from sqlmodel import SQLModel
from shared.db.session import engine
from shared.models.user import User
from shared.models.task import Task
from phase3.backend.app.models.conversation import Conversation
from phase3.backend.app.models.message import Message


def init_db():
    """Initialize the database and create tables"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
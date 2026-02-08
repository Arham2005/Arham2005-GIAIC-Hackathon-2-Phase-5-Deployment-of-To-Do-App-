#!/usr/bin/env python3
"""
Script to manually create a user in the database to bypass the model conflict issue
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Import database and user model
from shared.db.base import engine
from shared.models.user import User
from shared.models.task import Task
from sqlmodel import Session, select
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user_directly(email: str, password: str):
    """Create a user directly in the database"""

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create user instance
    user = User(
        email=email,
        hashed_password=hashed_password
    )

    # Add to database
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == email)).first()
        if existing_user:
            print(f"User {email} already exists!")
            return existing_user

        session.add(user)
        session.commit()
        session.refresh(user)
        print(f"User {email} created successfully with ID: {user.id}")
        return user

if __name__ == "__main__":
    # Create the user with the provided credentials
    email = "user1@gmail.com"
    password = "user112345"

    print(f"Creating user: {email}")
    user = create_user_directly(email, password)

    # Verify the user was created
    with Session(engine) as session:
        retrieved_user = session.exec(select(User).where(User.email == email)).first()
        if retrieved_user:
            print(f"✓ User {retrieved_user.email} verified in database with ID: {retrieved_user.id}")
        else:
            print("✗ Failed to verify user in database")
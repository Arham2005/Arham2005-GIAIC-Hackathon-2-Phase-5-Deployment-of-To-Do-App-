from typing import Optional
from sqlmodel import Session
from shared.models.user import User, UserCreate
import bcrypt
import jwt
from datetime import datetime, timedelta
from shared.core.config import settings
import logging

def hash_password(password: str) -> str:
    # Truncate password to 72 bytes to avoid bcrypt limitations
    truncated_password = password[:72] if len(password) > 72 else password
    # Hash the password using bcrypt directly
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(truncated_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate password to 72 bytes to avoid bcrypt limitations
    truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
    try:
        return bcrypt.checkpw(truncated_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, user_create: UserCreate) -> User:
    hashed_password = hash_password(user_create.password)
    db_user = User(email=user_create.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
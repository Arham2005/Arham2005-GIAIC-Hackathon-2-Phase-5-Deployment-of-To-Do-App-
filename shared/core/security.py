from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from shared.models.user import User
from shared.core.config import settings
import logging

# Suppress the bcrypt version warning
logging.getLogger("passlib").setLevel(logging.ERROR)

# Initialize bcrypt context with explicit backend settings to avoid runtime initialization issues
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__ident="2b",
    bcrypt__rounds=12
)

# Pre-initialize bcrypt backend to avoid runtime issues
try:
    pwd_context.hash("initialization_test")
except:
    # If initialization fails, we'll handle it during actual usage
    pass
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate password to 72 bytes if needed to avoid bcrypt limitations
    truncated_password = plain_password[:72] if len(plain_password) > 72 else plain_password
    return pwd_context.verify(truncated_password, hashed_password)


def hash_password(password: str) -> str:
    # Truncate password to 72 bytes if needed to avoid bcrypt limitations
    truncated_password = password[:72] if len(password) > 72 else password
    return pwd_context.hash(truncated_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return payload
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials,
    db: Session
) -> User:
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    user_email = payload.get("sub")  # Changed from "email" to "sub" to match token creation

    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = db.query(User).filter(User.email == user_email).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from shared.core.config import settings
from shared.models.user import User
from shared.db.session import engine
from shared.core.security import verify_token

security = HTTPBearer()

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = verify_token(token)  # Use the imported function from shared
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
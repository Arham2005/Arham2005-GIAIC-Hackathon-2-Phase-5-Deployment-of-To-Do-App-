from typing import Optional
from sqlmodel import Session
from shared.models.user import User, UserCreate
from shared.core.security import hash_password, verify_password, create_access_token


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
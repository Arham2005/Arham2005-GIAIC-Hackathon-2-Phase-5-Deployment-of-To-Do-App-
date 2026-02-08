from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    email: str
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserUpdate(SQLModel):
    email: Optional[str] = None
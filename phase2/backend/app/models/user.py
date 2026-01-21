from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .task import Task


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: list["Task"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    email: str
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime


class UserLogin(SQLModel):
    email: str
    password: str


class UserWithPassword(UserRead):
    hashed_password: str
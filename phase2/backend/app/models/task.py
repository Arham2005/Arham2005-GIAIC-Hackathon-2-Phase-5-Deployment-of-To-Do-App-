from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None


class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
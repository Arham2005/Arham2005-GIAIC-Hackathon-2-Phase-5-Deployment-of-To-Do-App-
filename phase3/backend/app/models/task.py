# from typing import Optional, List
# from sqlmodel import SQLModel, Field
# from datetime import datetime


# class TaskBase(SQLModel):
#     title: str
#     description: Optional[str] = None
#     completed: bool = False
#     priority: Optional[str] = "medium"  # low, medium, high, urgent
#     tags: Optional[List[str]] = []  # Store as JSON
#     due_date: Optional[datetime] = None
#     recurring: bool = False
#     recurrence_pattern: Optional[str] = None  # daily, weekly, monthly, yearly
#     parent_task_id: Optional[int] = None


# class Task(TaskBase, table=True):
#     __tablename__ = "tasks"

#     id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int = Field(foreign_key="users.id")
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: Optional[datetime] = Field(default=None)
#     reminder_sent: bool = False
#     parent_task_id: Optional[int] = Field(default=None)  # No foreign key constraint to avoid self-reference


# class TaskCreate(TaskBase):
#     title: str
#     description: Optional[str] = None
#     priority: Optional[str] = "medium"
#     tags: Optional[List[str]] = []
#     due_date: Optional[datetime] = None
#     recurring: bool = False
#     recurrence_pattern: Optional[str] = None
#     parent_task_id: Optional[int] = None


# class TaskRead(TaskBase):
#     id: int
#     user_id: int
#     created_at: datetime
#     updated_at: Optional[datetime] = None
#     reminder_sent: bool = False

#     class Config:
#         from_attributes = True


# class TaskUpdate(SQLModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     completed: Optional[bool] = None
#     priority: Optional[str] = None
#     tags: Optional[List[str]] = None
#     due_date: Optional[datetime] = None
#     recurring: Optional[bool] = None
#     recurrence_pattern: Optional[str] = None
#     parent_task_id: Optional[int] = None
#     reminder_sent: Optional[bool] = None


from typing import Optional, List
from datetime import datetime

from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON  # change if using another DB


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = "medium"  # low, medium, high, urgent

    # store list of tags as JSON in DB
    tags: Optional[List[str]] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )

    due_date: Optional[datetime] = None
    recurring: bool = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly, yearly
    parent_task_id: Optional[int] = None


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    reminder_sent: bool = False

    # kept without FK to avoid self-reference issues
    parent_task_id: Optional[int] = Field(default=None)


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    reminder_sent: bool = False

    class Config:
        from_attributes = True


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    parent_task_id: Optional[int] = None
    reminder_sent: Optional[bool] = None

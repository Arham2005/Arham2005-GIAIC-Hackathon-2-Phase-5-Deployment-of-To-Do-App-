from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy import Column, JSON
import json


class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = "medium"  # low, medium, high, urgent
    tags: Optional[str] = Field(default='[]')  # Store as JSON string
    due_date: Optional[datetime] = None
    recurring: bool = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly, yearly
    parent_task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    reminder_sent: bool = False

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    # Self-referencing relationship for parent/child tasks - FIXED
    parent_task: Optional["Task"] = Relationship(
        sa_relationship_kwargs={
            "remote_side": "[Task.id]",
            "foreign_keys": "[Task.parent_task_id]",
            "back_populates": "child_tasks"
        }
    )
    child_tasks: List["Task"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Task.id==Task.parent_task_id",
            "remote_side": "[Task.parent_task_id]",
            "back_populates": "parent_task",
            "overlaps": "parent_task"
        }
    )


class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = None  # Accept list but convert to JSON string
    due_date: Optional[datetime] = None
    recurring: bool = False
    recurrence_pattern: Optional[str] = None
    parent_task_id: Optional[int] = None


class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    reminder_sent: bool = False

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # Handle the case where tags might be a list instead of string
        # Create a temporary object with string tags to pass validation
        import copy

        # Check if tags is a list and handle accordingly
        original_tags = getattr(obj, 'tags', '[]')

        if isinstance(original_tags, list):
            # If tags is a list, temporarily convert to string for validation
            temp_obj = copy.copy(obj)
            temp_obj.tags = json.dumps(original_tags)

            # Now call the standard from_orm
            instance = super().from_orm(temp_obj)

            # Restore the original list format
            instance.tags = original_tags
        else:
            # If tags is already a string, proceed normally
            instance = super().from_orm(obj)

            # Convert string tags to list for the response
            if isinstance(instance.tags, str):
                try:
                    instance.tags = json.loads(instance.tags)
                except:
                    instance.tags = []

        return instance


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
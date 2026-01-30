from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False
    priority: Optional[str] = "medium"  # low, medium, high, urgent
    tags: Optional[List[str]] = []
    due_date: Optional[datetime] = None
    recurring: Optional[bool] = False
    recurrence_pattern: Optional[str] = None  # daily, weekly, monthly, yearly
    parent_task_id: Optional[int] = None


class TaskCreate(TaskBase):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    tags: Optional[List[str]] = []
    due_date: Optional[datetime] = None
    recurring: Optional[bool] = False
    recurrence_pattern: Optional[str] = None
    parent_task_id: Optional[int] = None


class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    reminder_sent: Optional[bool] = False

    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
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


class TaskFilter(BaseModel):
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    search_query: Optional[str] = None
    sort_by: Optional[str] = "created_at"  # created_at, due_date, priority
    sort_order: Optional[str] = "asc"  # asc, desc
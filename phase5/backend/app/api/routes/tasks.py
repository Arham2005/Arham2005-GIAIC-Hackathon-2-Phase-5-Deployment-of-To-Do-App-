from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...database import get_session
from ...models.task import TaskRead, TaskCreate, TaskUpdate
from ...services.task_service import TaskService
from ...api.deps import get_current_user
from ...models.user import User
from pydantic import BaseModel
from datetime import datetime


router = APIRouter()
task_service = TaskService()


class TaskFilterRequest(BaseModel):
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    search_query: Optional[str] = None
    sort_by: str = "created_at"
    sort_order: str = "asc"


@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create a new task with advanced features"""
    return task_service.create_task(db, task, current_user.id)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get a specific task"""
    task = task_service.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[TaskRead])
def get_tasks(
    filter_request: TaskFilterRequest = Depends(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all tasks for the current user with filters and sorting"""
    tasks = task_service.get_tasks(
        db=db,
        user_id=current_user.id,
        completed=filter_request.completed,
        priority=filter_request.priority,
        tags=filter_request.tags,
        due_date_from=filter_request.due_date_from,
        due_date_to=filter_request.due_date_to,
        search_query=filter_request.search_query,
        sort_by=filter_request.sort_by,
        sort_order=filter_request.sort_order
    )
    return tasks


@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update a specific task"""
    updated_task = task_service.update_task(db, task_id, task_update, current_user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete a specific task"""
    success = task_service.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/complete", response_model=TaskRead)
def mark_task_complete(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Mark a task as complete"""
    task = task_service.mark_complete(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/due-soon/", response_model=List[TaskRead])
def get_due_soon_tasks(
    days_ahead: int = 3,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get tasks that are due soon"""
    return task_service.get_due_soon_tasks(db, current_user.id, days_ahead)


@router.get("/recurring/", response_model=List[TaskRead])
def get_recurring_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all recurring tasks"""
    return task_service.get_recurring_tasks(db, current_user.id)
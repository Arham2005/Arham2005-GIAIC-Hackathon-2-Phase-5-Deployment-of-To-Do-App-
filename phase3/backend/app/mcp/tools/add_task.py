from typing import Dict, Any, Optional, List
from sqlmodel import Session
from datetime import datetime
from ...models.task import TaskCreate
from ...services.task_service import TaskService
from shared.models.user import User


def add_task_tool(
    user_id: str,
    title: str,
    description: str = "",
    priority: Optional[str] = "medium",
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
    recurring: Optional[bool] = False,
    recurrence_pattern: Optional[str] = None,
    parent_task_id: Optional[int] = None,
    db: Session = None
) -> Dict[str, Any]:
    """
    Add a new task for the user with advanced features.
    """
    if not user_id:
        raise ValueError("user_id is required to add a task")

    # Convert user_id to integer if it's passed as a string
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise ValueError(f"user_id must be numeric, got: {user_id}")

    # Parse due_date if provided
    due_date_obj = None
    if due_date:
        try:
            due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Invalid due_date format: {due_date}. Expected ISO format.")

    # Create task data with advanced features
    task_data = TaskCreate(
        title=title,
        description=description,
        priority=priority,
        tags=tags if tags else [],
        due_date=due_date_obj,
        recurring=recurring,
        recurrence_pattern=recurrence_pattern,
        parent_task_id=parent_task_id
    )

    # Create the task using the advanced task service
    task_service = TaskService()
    created_task = task_service.create_task(db, task_data, user_id_int)

    return {
        "task_id": created_task.id,
        "status": "created",
        "title": created_task.title,
        "priority": created_task.priority,
        "tags": created_task.tags,
        "due_date": created_task.due_date.isoformat() if created_task.due_date else None,
        "recurring": created_task.recurring,
        "recurrence_pattern": created_task.recurrence_pattern
    }
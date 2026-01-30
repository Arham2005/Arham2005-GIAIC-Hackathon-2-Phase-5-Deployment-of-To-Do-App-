from typing import List, Dict, Any, Optional
from sqlmodel import Session
from datetime import datetime
from ...models.task import TaskRead
from ...services.task_service import TaskService


def list_tasks_tool(
    user_id: str,
    status: str = "all",
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date_from: Optional[str] = None,
    due_date_to: Optional[str] = None,
    search_query: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "asc",
    db: Session = None
) -> List[Dict[str, Any]]:
    """
    List tasks for the user with advanced filtering and sorting options.
    """
    if not user_id:
        raise ValueError("user_id is required to list tasks")

    # Convert user_id to integer if it's passed as a string
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise ValueError(f"user_id must be numeric, got: {user_id}")

    # Parse date strings if provided
    due_date_from_obj = None
    due_date_to_obj = None
    if due_date_from:
        try:
            due_date_from_obj = datetime.fromisoformat(due_date_from.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Invalid due_date_from format: {due_date_from}. Expected ISO format.")

    if due_date_to:
        try:
            due_date_to_obj = datetime.fromisoformat(due_date_to.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Invalid due_date_to format: {due_date_to}. Expected ISO format.")

    # Determine completed filter based on status
    completed_filter = None
    if status == "pending":
        completed_filter = False
    elif status == "completed":
        completed_filter = True

    # Use the advanced task service
    task_service = TaskService()
    tasks = task_service.get_tasks(
        db=db,
        user_id=user_id_int,
        completed=completed_filter,
        priority=priority,
        tags=tags,
        due_date_from=due_date_from_obj,
        due_date_to=due_date_to_obj,
        search_query=search_query,
        sort_by=sort_by,
        sort_order=sort_order
    )

    # Convert tasks to dictionaries with all advanced fields
    tasks_list = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description or "",
            "completed": task.completed,
            "priority": task.priority,
            "tags": task.tags,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "recurring": task.recurring,
            "recurrence_pattern": task.recurrence_pattern,
            "parent_task_id": task.parent_task_id,
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
            "reminder_sent": task.reminder_sent
        }
        tasks_list.append(task_dict)

    return tasks_list
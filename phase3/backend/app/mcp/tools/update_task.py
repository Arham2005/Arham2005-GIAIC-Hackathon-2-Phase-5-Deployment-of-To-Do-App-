from typing import Dict, Any, Optional, List
from sqlmodel import Session
from datetime import datetime
from ...models.task import TaskUpdate
from ...services.task_service import TaskService


def update_task_tool(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date: Optional[str] = None,
    recurring: Optional[bool] = None,
    recurrence_pattern: Optional[str] = None,
    parent_task_id: Optional[int] = None,
    reminder_sent: Optional[bool] = None,
    db: Session = None
) -> Dict[str, Any]:
    """
    Update an existing task for the user with advanced features.
    """
    if not user_id:
        raise ValueError("user_id is required to update a task")

    # Convert user_id to integer if it's passed as a string
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise ValueError(f"user_id must be numeric, got: {user_id}")

    # Check if at least one field is provided
    if all(field is None for field in [
        title, description, completed, priority, tags, due_date,
        recurring, recurrence_pattern, parent_task_id, reminder_sent
    ]):
        raise ValueError("At least one field must be provided to update")

    # Parse due_date if provided
    due_date_obj = None
    if due_date:
        try:
            due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except ValueError:
            raise ValueError(f"Invalid due_date format: {due_date}. Expected ISO format.")

    # Create a TaskUpdate object with the provided fields
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if completed is not None:
        update_data["completed"] = completed
    if priority is not None:
        update_data["priority"] = priority
    if tags is not None:
        update_data["tags"] = tags
    if due_date_obj is not None:
        update_data["due_date"] = due_date_obj
    if recurring is not None:
        update_data["recurring"] = recurring
    if recurrence_pattern is not None:
        update_data["recurrence_pattern"] = recurrence_pattern
    if parent_task_id is not None:
        update_data["parent_task_id"] = parent_task_id
    if reminder_sent is not None:
        update_data["reminder_sent"] = reminder_sent

    task_update = TaskUpdate(**update_data)

    # Use the advanced task service to update the task
    task_service = TaskService()
    updated_task = task_service.update_task(db, task_id, task_update, user_id_int)

    if updated_task:
        return {
            "task_id": updated_task.id,
            "status": "updated",
            "title": updated_task.title,
            "completed": updated_task.completed,
            "priority": updated_task.priority,
            "tags": updated_task.tags,
            "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
            "recurring": updated_task.recurring,
            "recurrence_pattern": updated_task.recurrence_pattern,
            "parent_task_id": updated_task.parent_task_id,
            "reminder_sent": updated_task.reminder_sent
        }
    else:
        raise ValueError(f"Task {task_id} not found or could not be updated")
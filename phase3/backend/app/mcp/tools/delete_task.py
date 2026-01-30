from typing import Dict, Any
from sqlmodel import Session
from ...services.task_service import TaskService


def delete_task_tool(user_id: str, task_id: int, db: Session = None) -> Dict[str, Any]:
    """
    Delete a task for the user.
    """
    if not user_id:
        raise ValueError("user_id is required to delete a task")

    # Convert user_id to integer if it's passed as a string
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise ValueError(f"user_id must be numeric, got: {user_id}")

    # Use the advanced task service
    task_service = TaskService()

    # Get the task first to return its title
    task = task_service.get_task(db, task_id, user_id_int)
    if not task:
        raise ValueError(f"Task {task_id} not found or could not be deleted")

    # Delete the task using the task service
    success = task_service.delete_task(db, task_id, user_id_int)

    if success:
        return {
            "task_id": task_id,
            "status": "deleted",
            "title": task.title
        }
    else:
        raise ValueError(f"Task {task_id} not found or could not be deleted")
from typing import Dict, Any
from sqlmodel import Session
from phase2.backend.app.services.task_service import complete_task


def complete_task_tool(user_id: str, task_id: int, db: Session = None) -> Dict[str, Any]:
    """
    Mark a task as complete for the user.
    """
    if not user_id:
        raise ValueError("user_id is required to complete a task")

    # Convert user_id to integer if it's passed as a string
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise ValueError(f"user_id must be numeric, got: {user_id}")

    # Complete the task using the task service
    updated_task = complete_task(db, task_id, user_id_int)

    if updated_task:
        return {
            "task_id": updated_task.id,
            "status": "completed",
            "title": updated_task.title
        }
    else:
        raise ValueError(f"Task {task_id} not found or could not be completed")
from typing import Dict, Any
from sqlmodel import Session
from shared.models.task import TaskUpdate
from phase2.backend.app.services.task_service import update_task


def update_task_tool(task_id: int, fields: Dict[str, Any], user_id: int = None, db: Session = None) -> Dict[str, Any]:
    """
    Update an existing task for the user.
    """
    if not user_id:
        raise ValueError("user_id is required to update a task")

    if not fields:
        raise ValueError("At least one field must be provided to update")

    # Create a TaskUpdate object with the provided fields
    task_update = TaskUpdate(**{k: v for k, v in fields.items() if v is not None})

    # Update the task using the task service
    updated_task = update_task(db, task_id, task_update, user_id)

    if updated_task:
        return {
            "success": True,
            "message": f"Task {task_id} has been updated successfully",
            "task_id": updated_task.id,
            "updated_fields": list(fields.keys())
        }
    else:
        return {
            "success": False,
            "message": f"Task {task_id} not found or could not be updated"
        }
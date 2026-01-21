from typing import Dict, Any
from sqlmodel import Session
from phase2.backend.app.services.task_service import complete_task


def complete_task_tool(task_id: int, user_id: int = None, db: Session = None) -> Dict[str, Any]:
    """
    Mark a task as complete for the user.
    """
    if not user_id:
        raise ValueError("user_id is required to complete a task")

    # Complete the task using the task service
    updated_task = complete_task(db, task_id, user_id)

    if updated_task:
        return {
            "success": True,
            "message": f"Task {task_id} has been marked as complete",
            "task_id": updated_task.id,
            "completed": updated_task.completed
        }
    else:
        return {
            "success": False,
            "message": f"Task {task_id} not found or could not be completed"
        }
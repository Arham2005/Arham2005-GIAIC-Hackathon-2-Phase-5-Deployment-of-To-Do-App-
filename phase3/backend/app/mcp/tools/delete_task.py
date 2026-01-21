from typing import Dict, Any
from sqlmodel import Session
from phase2.backend.app.services.task_service import delete_task


def delete_task_tool(task_id: int, user_id: int = None, db: Session = None) -> Dict[str, Any]:
    """
    Delete a task for the user.
    """
    if not user_id:
        raise ValueError("user_id is required to delete a task")

    # Delete the task using the task service
    success = delete_task(db, task_id, user_id)

    if success:
        return {
            "success": True,
            "message": f"Task {task_id} has been deleted successfully"
        }
    else:
        return {
            "success": False,
            "message": f"Task {task_id} not found or could not be deleted"
        }
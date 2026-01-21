from typing import Dict, Any
from sqlmodel import Session
from shared.models.task import TaskCreate
from phase2.backend.app.services.task_service import create_task
from shared.models.user import User


def add_task_tool(title: str, description: str = "", user_id: int = None, db: Session = None) -> Dict[str, Any]:
    """
    Add a new task for the user.
    """
    if not user_id:
        raise ValueError("user_id is required to add a task")

    # Create task data
    task_data = TaskCreate(title=title, description=description)

    # Create the task using the task service
    created_task = create_task(db, task_data, user_id)

    return {
        "success": True,
        "message": f"Task '{created_task.title}' has been added successfully",
        "task_id": created_task.id,
        "task_title": created_task.title
    }
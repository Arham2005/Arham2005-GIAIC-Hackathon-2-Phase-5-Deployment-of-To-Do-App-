from typing import List, Dict, Any
from sqlmodel import Session
from shared.models.task import TaskRead
from phase2.backend.app.services.task_service import get_tasks


def list_tasks_tool(user_id: int, db: Session = None) -> List[Dict[str, Any]]:
    """
    List all tasks for the user.
    """
    if not user_id:
        raise ValueError("user_id is required to list tasks")

    # Get tasks for the user
    tasks = get_tasks(db, user_id)

    # Convert tasks to dictionaries
    tasks_list = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description or "",
            "completed": task.completed,
            "created_at": task.created_at.isoformat() if task.created_at else None
        }
        tasks_list.append(task_dict)

    return tasks_list
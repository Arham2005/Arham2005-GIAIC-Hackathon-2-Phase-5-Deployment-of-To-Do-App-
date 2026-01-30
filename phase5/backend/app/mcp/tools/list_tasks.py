from typing import Optional, List
from datetime import datetime
from ...services.task_service import TaskService


async def list_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = [],
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    search_query: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "asc"
):
    """
    List tasks with advanced filtering and sorting

    Args:
        completed: Filter by completion status
        priority: Filter by priority level
        tags: Filter by tags
        due_date_from: Filter tasks with due date after this date
        due_date_to: Filter tasks with due date before this date
        search_query: Search in title and description
        sort_by: Field to sort by (created_at, due_date, priority)
        sort_order: Sort order (asc, desc)
    """
    from ...database import get_session
    from ...api.deps import get_current_user

    # Get current user (in a real implementation, this would come from context)
    # For now, assuming user_id 1 for demonstration
    user_id = 1

    async with get_session() as session:
        task_service = TaskService()

        tasks = task_service.get_tasks(
            db=session,
            user_id=user_id,
            completed=completed,
            priority=priority,
            tags=tags if tags else [],
            due_date_from=due_date_from,
            due_date_to=due_date_to,
            search_query=search_query,
            sort_by=sort_by,
            sort_order=sort_order
        )

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "tags": task.tags,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "recurring": task.recurring,
                "recurrence_pattern": task.recurrence_pattern,
                "parent_task_id": task.parent_task_id,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat() if task.updated_at else None
            }
            for task in tasks
        ]


# Define the tool schema for MCP
list_tasks_schema = {
    "name": "list_tasks",
    "description": "List tasks with advanced filtering and sorting",
    "input_schema": {
        "type": "object",
        "properties": {
            "completed": {
                "type": "boolean",
                "description": "Filter by completion status"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "urgent"],
                "description": "Filter by priority level"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Filter by tags"
            },
            "due_date_from": {
                "type": "string",
                "format": "date-time",
                "description": "Filter tasks with due date after this date"
            },
            "due_date_to": {
                "type": "string",
                "format": "date-time",
                "description": "Filter tasks with due date before this date"
            },
            "search_query": {
                "type": "string",
                "description": "Search in title and description"
            },
            "sort_by": {
                "type": "string",
                "enum": ["created_at", "due_date", "priority"],
                "description": "Field to sort by",
                "default": "created_at"
            },
            "sort_order": {
                "type": "string",
                "enum": ["asc", "desc"],
                "description": "Sort order",
                "default": "asc"
            }
        }
    }
}
from typing import Optional, List
from datetime import datetime
from ...services.task_service import TaskService
from ...models.task import TaskCreate


async def add_task(
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = "medium",
    tags: Optional[List[str]] = [],
    due_date: Optional[datetime] = None,
    recurring: Optional[bool] = False,
    recurrence_pattern: Optional[str] = None,
    parent_task_id: Optional[int] = None
):
    """
    Add a new task with advanced features

    Args:
        title: Task title
        description: Task description
        priority: Task priority (low, medium, high, urgent)
        tags: List of tags for the task
        due_date: Due date for the task
        recurring: Whether the task is recurring
        recurrence_pattern: Recurrence pattern (daily, weekly, monthly, yearly)
        parent_task_id: ID of parent task if this is a subtask
    """
    from ...database import get_session
    from ...api.deps import get_current_user

    # Get current user (in a real implementation, this would come from context)
    # For now, assuming user_id 1 for demonstration
    user_id = 1

    async with get_session() as session:
        task_service = TaskService()

        task_create = TaskCreate(
            title=title,
            description=description,
            priority=priority,
            tags=tags if tags else [],
            due_date=due_date,
            recurring=recurring,
            recurrence_pattern=recurrence_pattern,
            parent_task_id=parent_task_id
        )

        created_task = task_service.create_task(session, task_create, user_id)

        # Send event to Kafka
        from ..kafka.producer import kafka_producer
        await kafka_producer.send_task_event("task_created", created_task.dict())

        # Send event to Dapr
        from ..dapr.client import dapr_client
        await dapr_client.publish_event("pubsub", "task-created", created_task.dict())

        return {
            "id": created_task.id,
            "title": created_task.title,
            "description": created_task.description,
            "completed": created_task.completed,
            "priority": created_task.priority,
            "tags": created_task.tags,
            "due_date": created_task.due_date.isoformat() if created_task.due_date else None,
            "recurring": created_task.recurring,
            "recurrence_pattern": created_task.recurrence_pattern,
            "parent_task_id": created_task.parent_task_id
        }


# Define the tool schema for MCP
add_task_schema = {
    "name": "add_task",
    "description": "Add a new task with advanced features",
    "input_schema": {
        "type": "object",
        "properties": {
            "title": {
                "type": "string",
                "description": "Task title"
            },
            "description": {
                "type": "string",
                "description": "Task description"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "urgent"],
                "description": "Task priority level",
                "default": "medium"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of tags for the task"
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "Due date for the task in ISO format"
            },
            "recurring": {
                "type": "boolean",
                "description": "Whether the task is recurring",
                "default": False
            },
            "recurrence_pattern": {
                "type": "string",
                "enum": ["daily", "weekly", "monthly", "yearly"],
                "description": "Recurrence pattern for recurring tasks"
            },
            "parent_task_id": {
                "type": "integer",
                "description": "ID of parent task if this is a subtask"
            }
        },
        "required": ["title"]
    }
}
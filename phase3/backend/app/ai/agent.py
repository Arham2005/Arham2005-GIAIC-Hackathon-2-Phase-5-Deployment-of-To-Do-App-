from typing import Dict, Any
from sqlmodel import Session
from ..mcp.server import MCPServer
from ..mcp.tools.add_task import add_task_tool
from ..mcp.tools.list_tasks import list_tasks_tool
from ..mcp.tools.update_task import update_task_tool
from ..mcp.tools.complete_task import complete_task_tool
from ..mcp.tools.delete_task import delete_task_tool
import json
import re
from datetime import datetime


def setup_mcp_server(db: Session) -> MCPServer:
    """
    Setup MCP server with all tools properly configured for OpenAI integration
    """
    mcp_server = MCPServer(db)

    # Register add_task tool with advanced parameters
    add_task_params = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The user ID"
            },
            "title": {
                "type": "string",
                "description": "The title of the task to add"
            },
            "description": {
                "type": "string",
                "description": "The description of the task to add (optional)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "urgent"],
                "description": "Task priority level (optional)",
                "default": "medium"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of tags for the task (optional)"
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "Due date for the task in ISO format (optional)"
            },
            "recurring": {
                "type": "boolean",
                "description": "Whether the task is recurring (optional)",
                "default": False
            },
            "recurrence_pattern": {
                "type": "string",
                "enum": ["daily", "weekly", "monthly", "yearly"],
                "description": "Recurrence pattern for recurring tasks (optional)"
            },
            "parent_task_id": {
                "type": "integer",
                "description": "ID of parent task if this is a subtask (optional)"
            }
        },
        "required": ["user_id", "title"]
    }
    mcp_server.register_tool("add_task", add_task_tool, "Add a new task for the user with advanced features", add_task_params)

    # Register list_tasks tool with advanced parameters
    list_tasks_params = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The user ID"
            },
            "status": {
                "type": "string",
                "description": "Filter tasks by completion status (all, pending, completed)",
                "enum": ["all", "pending", "completed"]
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "urgent"],
                "description": "Filter tasks by priority level (optional)"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Filter tasks by tags (optional)"
            },
            "due_date_from": {
                "type": "string",
                "format": "date-time",
                "description": "Filter tasks with due date after this date (optional)"
            },
            "due_date_to": {
                "type": "string",
                "format": "date-time",
                "description": "Filter tasks with due date before this date (optional)"
            },
            "search_query": {
                "type": "string",
                "description": "Search in title and description (optional)"
            },
            "sort_by": {
                "type": "string",
                "enum": ["created_at", "due_date", "priority"],
                "description": "Field to sort by (optional)",
                "default": "created_at"
            },
            "sort_order": {
                "type": "string",
                "enum": ["asc", "desc"],
                "description": "Sort order (optional)",
                "default": "asc"
            }
        },
        "required": ["user_id"]
    }
    mcp_server.register_tool("list_tasks", list_tasks_tool, "List tasks for the user with advanced filtering and sorting", list_tasks_params)

    # Register update_task tool with advanced parameters
    update_task_params = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The user ID"
            },
            "task_id": {
                "type": "integer",
                "description": "The ID of the task to update"
            },
            "title": {
                "type": "string",
                "description": "The new title for the task (optional)"
            },
            "description": {
                "type": "string",
                "description": "The new description for the task (optional)"
            },
            "completed": {
                "type": "boolean",
                "description": "Whether the task is completed (optional)"
            },
            "priority": {
                "type": "string",
                "enum": ["low", "medium", "high", "urgent"],
                "description": "New priority level for the task (optional)"
            },
            "tags": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "New tags for the task (optional)"
            },
            "due_date": {
                "type": "string",
                "format": "date-time",
                "description": "New due date for the task in ISO format (optional)"
            },
            "recurring": {
                "type": "boolean",
                "description": "Whether the task is recurring (optional)"
            },
            "recurrence_pattern": {
                "type": "string",
                "enum": ["daily", "weekly", "monthly", "yearly"],
                "description": "Recurrence pattern for recurring tasks (optional)"
            },
            "parent_task_id": {
                "type": "integer",
                "description": "New parent task ID if this is a subtask (optional)"
            },
            "reminder_sent": {
                "type": "boolean",
                "description": "Whether a reminder has been sent (optional)"
            }
        },
        "required": ["user_id", "task_id"]
    }
    mcp_server.register_tool("update_task", update_task_tool, "Update an existing task for the user with advanced features", update_task_params)

    # Register complete_task tool with proper parameters
    complete_task_params = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The user ID"
            },
            "task_id": {
                "type": "integer",
                "description": "The ID of the task to complete"
            }
        },
        "required": ["user_id", "task_id"]
    }
    mcp_server.register_tool("complete_task", complete_task_tool, "Mark a task as complete for the user", complete_task_params)

    # Register delete_task tool with proper parameters
    delete_task_params = {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "string",
                "description": "The user ID"
            },
            "task_id": {
                "type": "integer",
                "description": "The ID of the task to delete"
            }
        },
        "required": ["user_id", "task_id"]
    }
    mcp_server.register_tool("delete_task", delete_task_tool, "Delete a task for the user", delete_task_params)

    return mcp_server


def process_user_message(message: str, user_id: int, db: Session) -> Dict[str, Any]:
    """
    Process a user message using the AI agent and return an appropriate response.
    The agent will analyze the message and potentially call MCP tools to perform actions.
    Returns a dictionary with the response and any tool calls made.
    """

    # Setup MCP Server with properly configured tools
    mcp_server = setup_mcp_server(db)

    # Analyze the user message to determine intent
    intent = analyze_intent(message)

    # Process based on intent
    if intent == "add_task":
        response = handle_add_task(message, user_id, db, mcp_server)
    elif intent == "list_tasks":
        response = handle_list_tasks(message, user_id, db, mcp_server)
    elif intent == "update_task":
        response = handle_update_task(message, user_id, db, mcp_server)
    elif intent == "complete_task":
        response = handle_complete_task(message, user_id, db, mcp_server)
    elif intent == "delete_task":
        response = handle_delete_task(message, user_id, db, mcp_server)
    else:
        response = handle_general_query(message, user_id, db, mcp_server)

    # Return response with empty tool_calls for now
    # In a real OpenAI integration, we would return actual tool calls
    return {
        "response": response,
        "tool_calls": []  # Will be populated when using actual OpenAI integration
    }


def analyze_intent(message: str) -> str:
    """
    Analyze the user message to determine the intent.
    Order matters - check more specific intents first
    """
    message_lower = message.lower().strip()

    # Define patterns for different intents - order matters
    if any(word in message_lower for word in ["update", "change", "modify", "edit"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "update_task"

    if any(word in message_lower for word in ["add", "create", "new", "make"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "add_task"

    if any(word in message_lower for word in ["list", "show", "display", "view", "get"]):
        if any(word in message_lower for word in ["task", "todo", "item", "all"]):
            return "list_tasks"

    if any(word in message_lower for word in ["complete", "done", "finish", "mark"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "complete_task"

    if any(word in message_lower for word in ["delete", "remove", "erase", "cancel"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "delete_task"

    # Default to general query
    return "general"


def handle_add_task(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle adding a new task based on the user's message.
    """
    # Extract task title and description from the message
    title_match = re.search(r"(?:add|create|make)\s+(?:a\s+)?(?:task|todo|item)\s+(?:named|called|titled)?\s*(.+?)(?:\s+with\s+description\s+(.+))?$", message.lower())

    if not title_match:
        # Try alternative patterns
        title_match = re.search(r"(?:add|create|make)\s+(.+?)(?:\s+and|\.|$)", message.lower())

    if title_match:
        title = title_match.group(1).strip()
        # Clean up the title
        title = re.sub(r'(?:named|called|titled)\s+', '', title)

        # Try to extract description if present
        description = None
        if len(title_match.groups()) > 1 and title_match.group(2):
            description = title_match.group(2).strip()

        # Prepare arguments for the tool
        tool_args = {
            "title": title,
            "description": description or "",
            "user_id": str(user_id)  # Convert to string as expected by new tool
        }

        try:
            result = mcp_server.call_tool("add_task", tool_args)
            return f"I've added the task '{result['title']}' to your list with ID {result['task_id']}."
        except Exception as e:
            return f"Sorry, I couldn't add the task. Error: {str(e)}"
    else:
        return "I couldn't understand what task you want to add. Please specify the task title."


def handle_list_tasks(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle listing tasks based on the user's message.
    """
    # Determine status filter from message
    status = "all"
    if "pending" in message.lower() or "incomplete" in message.lower():
        status = "pending"
    elif "completed" in message.lower() or "done" in message.lower():
        status = "completed"

    try:
        result = mcp_server.call_tool("list_tasks", {"user_id": str(user_id), "status": status})

        if isinstance(result, list) and len(result) == 0:
            return "You don't have any tasks yet. You can add some tasks!"
        else:
            task_list = []
            for task in result:
                status_text = "✓" if task['completed'] else "○"
                task_str = f"{status_text} [{task['id']}] {task['title']}"
                if task.get('description'):
                    task_str += f" - {task['description']}"
                task_list.append(task_str)

            status_label = status if status != "all" else "all"
            return f"Here are your {status_label} tasks:\n" + "\n".join([f"  {task}" for task in task_list])
    except Exception as e:
        return f"Sorry, I couldn't retrieve your tasks. Error: {str(e)}"


def handle_update_task(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle updating a task based on the user's message.
    """
    # Extract task ID and update information
    # Look for patterns like "update task 1 to have title 'new title'" or "update task 1 to have description '...'"
    id_match = re.search(r"(?:update|change|modify|edit)\s+task\s+(\d+)", message.lower())

    if id_match:
        task_id = int(id_match.group(1))

        # Extract new title and description
        title_match = re.search(r"(?:title|name|to)\s+(?:is\s+|to\s+have\s+)?['\"](.+?)['\"]", message)
        desc_match = re.search(r"(?:to\s+have\s+)?(?:description|desc|details)\s+(?:is\s+|to\s+have\s+)?['\"](.+?)['\"]", message)

        update_args = {"user_id": str(user_id), "task_id": task_id}
        if title_match:
            update_args["title"] = title_match.group(1)
        if desc_match:
            update_args["description"] = desc_match.group(1)

        if "title" in update_args or "description" in update_args:
            try:
                result = mcp_server.call_tool("update_task", update_args)
                return f"I've updated task {result['task_id']} to '{result['title']}'."
            except Exception as e:
                return f"Sorry, I couldn't update the task. Error: {str(e)}"
        else:
            return f"I need more information to update task {task_id}. Please specify what you'd like to change."
    else:
        return "I couldn't identify which task you want to update. Please specify the task number."


def handle_complete_task(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle completing a task based on the user's message.
    """
    # Extract task ID
    id_match = re.search(r"(?:complete|done|finish|mark)\s+task\s+(\d+)", message.lower())

    if id_match:
        task_id = int(id_match.group(1))

        try:
            result = mcp_server.call_tool("complete_task", {
                "task_id": task_id,
                "user_id": str(user_id)
            })
            return f"I've marked task {result['task_id']} '{result['title']}' as complete."
        except Exception as e:
            return f"Sorry, I couldn't complete the task. Error: {str(e)}"
    else:
        return "I couldn't identify which task you want to mark as complete. Please specify the task number."


def handle_delete_task(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle deleting a task based on the user's message.
    """
    # Extract task ID
    id_match = re.search(r"(?:delete|remove|erase|cancel)\s+task\s+(\d+)", message.lower())

    if id_match:
        task_id = int(id_match.group(1))

        try:
            result = mcp_server.call_tool("delete_task", {
                "task_id": task_id,
                "user_id": str(user_id)
            })
            return f"I've deleted task {result['task_id']} '{result['title']}'."
        except Exception as e:
            return f"Sorry, I couldn't delete the task. Error: {str(e)}"
    else:
        return "I couldn't identify which task you want to delete. Please specify the task number."


def handle_general_query(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle general queries that don't map to specific actions.
    """
    message_lower = message.lower().strip()

    # Check for specific phrases rather than just substrings
    if any(greeting in message_lower for greeting in ["hello", "hi", "hey"]):
        return "Hi there! I'm your AI assistant for managing tasks. You can ask me to add, list, update, complete, or delete tasks."
    elif "help" in message_lower:
        return "I can help you with your tasks! You can ask me to: add a task, list your tasks, update a task, complete a task, or delete a task."
    elif any(thanks in message_lower for thanks in ["thank you", "thanks"]):
        return "You're welcome! Let me know if there's anything else I can help you with."
    elif "what time is it" in message_lower or "what's the time" in message_lower:
        return f"The current time is {datetime.now().strftime('%H:%M %p')}."
    elif "what date is it" in message_lower or "what's the date" in message_lower or "today's date" in message_lower:
        return f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."

    return f"I'm not sure how to help with that. You can ask me to add, list, update, complete, or delete tasks. Your message: '{message}'"
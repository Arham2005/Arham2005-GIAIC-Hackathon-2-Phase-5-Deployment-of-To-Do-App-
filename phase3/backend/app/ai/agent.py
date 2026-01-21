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


def process_user_message(message: str, user_id: int, db: Session) -> str:
    """
    Process a user message using the AI agent and return an appropriate response.
    The agent will analyze the message and potentially call MCP tools to perform actions.
    """

    # Initialize MCP Server with the user's tools
    mcp_server = MCPServer(db)

    # Register all available tools
    mcp_server.register_tool("add_task", add_task_tool)
    mcp_server.register_tool("list_tasks", list_tasks_tool)
    mcp_server.register_tool("update_task", update_task_tool)
    mcp_server.register_tool("complete_task", complete_task_tool)
    mcp_server.register_tool("delete_task", delete_task_tool)

    # Analyze the user message to determine intent
    intent = analyze_intent(message)

    # Process based on intent
    if intent == "add_task":
        return handle_add_task(message, user_id, db, mcp_server)
    elif intent == "list_tasks":
        return handle_list_tasks(message, user_id, db, mcp_server)
    elif intent == "update_task":
        return handle_update_task(message, user_id, db, mcp_server)
    elif intent == "complete_task":
        return handle_complete_task(message, user_id, db, mcp_server)
    elif intent == "delete_task":
        return handle_delete_task(message, user_id, db, mcp_server)
    else:
        return handle_general_query(message, user_id, db, mcp_server)


def analyze_intent(message: str) -> str:
    """
    Analyze the user message to determine the intent.
    """
    message_lower = message.lower().strip()

    # Define patterns for different intents
    if any(word in message_lower for word in ["add", "create", "new", "make"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "add_task"

    if any(word in message_lower for word in ["list", "show", "display", "view", "get"]):
        if any(word in message_lower for word in ["task", "todo", "item", "all"]):
            return "list_tasks"

    if any(word in message_lower for word in ["update", "change", "modify", "edit"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "update_task"

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
            "user_id": user_id
        }

        try:
            result = mcp_server.call_tool("add_task", tool_args)
            return f"I've added the task '{title}' to your list. {result}"
        except Exception as e:
            return f"Sorry, I couldn't add the task. Error: {str(e)}"
    else:
        return "I couldn't understand what task you want to add. Please specify the task title."


def handle_list_tasks(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle listing tasks based on the user's message.
    """
    try:
        result = mcp_server.call_tool("list_tasks", {"user_id": user_id})

        if isinstance(result, list) and len(result) == 0:
            return "You don't have any tasks yet. You can add some tasks!"
        else:
            task_list = "\n".join([f"- {task['title']}" + (f" ({task['description']})" if task.get('description') else "") for task in result])
            return f"Here are your tasks:\n{task_list}"
    except Exception as e:
        return f"Sorry, I couldn't retrieve your tasks. Error: {str(e)}"


def handle_update_task(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle updating a task based on the user's message.
    """
    # Extract task ID and update information
    # Look for patterns like "update task 1 to have title 'new title'"
    id_match = re.search(r"(?:update|change|modify|edit)\s+task\s+(\d+)", message.lower())

    if id_match:
        task_id = int(id_match.group(1))

        # Extract new title and description
        title_match = re.search(r"(?:title|name|to)\s+(?:is\s+)?['\"](.+?)['\"]", message)
        desc_match = re.search(r"(?:description|desc|details)\s+(?:is\s+)?['\"](.+?)['\"]", message)

        update_fields = {}
        if title_match:
            update_fields["title"] = title_match.group(1)
        if desc_match:
            update_fields["description"] = desc_match.group(1)

        if update_fields:
            try:
                result = mcp_server.call_tool("update_task", {
                    "task_id": task_id,
                    "fields": update_fields,
                    "user_id": user_id
                })
                return f"I've updated task {task_id}. {result}"
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
                "user_id": user_id
            })
            return f"I've marked task {task_id} as complete. {result}"
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
                "user_id": user_id
            })
            return f"I've deleted task {task_id}. {result}"
        except Exception as e:
            return f"Sorry, I couldn't delete the task. Error: {str(e)}"
    else:
        return "I couldn't identify which task you want to delete. Please specify the task number."


def handle_general_query(message: str, user_id: int, db: Session, mcp_server: MCPServer) -> str:
    """
    Handle general queries that don't map to specific actions.
    """
    responses = {
        "hello": "Hi there! I'm your AI assistant for managing tasks. You can ask me to add, list, update, complete, or delete tasks.",
        "hi": "Hello! I'm here to help you manage your tasks. Just let me know what you'd like to do!",
        "help": "I can help you with your tasks! You can ask me to: add a task, list your tasks, update a task, complete a task, or delete a task.",
        "thank you": "You're welcome! Let me know if there's anything else I can help you with.",
        "thanks": "You're welcome! Feel free to ask me anything else."
    }

    message_lower = message.lower().strip()

    for trigger, response in responses.items():
        if trigger in message_lower:
            return response

    return f"I'm not sure how to help with that. You can ask me to add, list, update, complete, or delete tasks. Your message: '{message}'"
"""
Enhanced Chat Service for AI Task Management
==========================================

This module provides enhanced natural language processing for the chatbot
to properly handle task management commands and integrate with backend services.
"""
import re
from typing import Dict, Any, List, Tuple
from sqlmodel import Session
from datetime import datetime, timedelta
import json
import logging

logger = logging.getLogger(__name__)

# Simple in-memory storage for conversations (in production, use proper database)
conversations_db = {}
messages_db = {}
next_conv_id = 1
next_msg_id = 1


def create_conversation(user_id: int, title: str) -> Dict[str, Any]:
    global next_conv_id
    conv_id = next_conv_id
    next_conv_id += 1

    conversation = {
        "id": conv_id,
        "title": title,
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat()
    }

    conversations_db[conv_id] = conversation
    messages_db[conv_id] = []

    return conversation


def add_message_to_conversation(conversation_id: int, content: str, role: str, user_id: int) -> Dict[str, Any]:
    global next_msg_id
    msg_id = next_msg_id
    next_msg_id += 1

    message = {
        "id": msg_id,
        "content": content,
        "role": role,
        "conversation_id": conversation_id,
        "user_id": user_id,
        "created_at": datetime.utcnow().isoformat()
    }

    if conversation_id not in messages_db:
        messages_db[conversation_id] = []

    messages_db[conversation_id].append(message)
    return message


def get_conversation_messages(conversation_id: int) -> List[Dict[str, Any]]:
    return messages_db.get(conversation_id, [])


def extract_task_details(text: str) -> Dict[str, Any]:
    """Extract task details from natural language text"""
    text_lower = text.lower().strip()

    # Initialize defaults
    result = {
        "title": "",
        "priority": "medium",
        "due_date": None,
        "tags": [],
        "recurring": False,
        "recurrence_pattern": None
    }

    # Extract task title - look for patterns like "add task to X", "create task X", etc.
    title_patterns = [
        r'(?:add|create|make|new|set up)\s+(?:a\s+)?(?:task|todo|to-do)\s+(?:called\s+|named\s+|to\s+|for\s+|about\s+)?(.+?)(?:\s+with|\s+and|\s+by|\s+on|\s+due|\s+every|\s+monthly|\s+weekly|\s+daily|\s+$)',
        r'(?:add|create|make|new|set up)\s+(?:a\s+)?(.+?)(?:\s+with|\s+and|\s+by|\s+on|\s+due|\s+every|\s+monthly|\s+weekly|\s+daily|\s+$)',
        r'task[:\s]+(.+?)(?:\s+with|\s+and|\s+by|\s+on|\s+due|\s+every|\s+monthly|\s+weekly|\s+daily|\s+$)'
    ]

    for pattern in title_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            result["title"] = match.group(1).strip()
            break

    # If no title found, try to extract from the whole text
    if not result["title"]:
        # Remove common verbs and extract main content
        result["title"] = text.strip()
        # Clean up common phrases
        for phrase in ['add a task', 'create a task', 'add task', 'create task', 'new task']:
            result["title"] = re.sub(phrase, '', result["title"], flags=re.IGNORECASE).strip()

    # Determine priority
    if any(word in text_lower for word in ['urgent', 'critical', 'emergency', 'asap', 'immediately']):
        result["priority"] = "urgent"
    elif any(word in text_lower for word in ['high', 'important', 'priority', 'crucial']):
        result["priority"] = "high"
    elif any(word in text_lower for word in ['low', 'minor', 'optional']):
        result["priority"] = "low"

    # Extract due dates
    date_patterns = [
        r'to\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
        r'by\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
        r'on\s+\w+\s+\d{1,2}(?:st|nd|rd|th)?',
        r'due\s+(?:tomorrow|today|this week|next week|this month|next month)',
        r'tomorrow',
        r'today',
        r'next\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
        r'this\s+(?:week|month|year)'
    ]

    for pattern in date_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            date_text = match.group(0)
            # Convert to actual date (simplified)
            if 'today' in date_text:
                result["due_date"] = datetime.now().strftime('%Y-%m-%d')
            elif 'tomorrow' in date_text:
                result["due_date"] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            elif 'monday' in date_text:
                # Calculate next Monday
                today = datetime.now()
                days_ahead = 0 if today.weekday() == 0 else 7 - today.weekday()
                if today.weekday() == 0:  # If today is Monday, get next Monday
                    days_ahead = 7
                next_monday = today + timedelta(days_ahead)
                result["due_date"] = next_monday.strftime('%Y-%m-%d')
            # Add more date calculations as needed

    # Extract tags
    tag_patterns = [
        r'tags?\s+(.+?)(?:\s+and|\s+or|\s+with|\s*$)',
        r'with\s+tags?\s+(.+?)(?:\s+and|\s+or|\s+with|\s*$)',
        r'labeled\s+as\s+(.+?)(?:\s+and|\s+or|\s+with|\s*$)'
    ]

    for pattern in tag_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            tags_text = match.group(1)
            # Split by commas, 'and', 'or'
            tags = re.split(r',|\s+and\s+|\s+or\s+', tags_text)
            result["tags"] = [tag.strip() for tag in tags if tag.strip()]
            break

    # Extract recurring patterns
    if any(word in text_lower for word in ['every day', 'daily', 'each day']):
        result["recurring"] = True
        result["recurrence_pattern"] = "daily"
    elif any(word in text_lower for word in ['every week', 'weekly', 'each week', 'every monday', 'every tuesday', 'every wednesday', 'every thursday', 'every friday', 'every saturday', 'every sunday']):
        result["recurring"] = True
        result["recurrence_pattern"] = "weekly"
    elif any(word in text_lower for word in ['every month', 'monthly', 'each month']):
        result["recurring"] = True
        result["recurrence_pattern"] = "monthly"
    elif any(word in text_lower for word in ['every year', 'yearly', 'each year']):
        result["recurring"] = True
        result["recurrence_pattern"] = "yearly"

    # Clean up title
    if not result["title"].strip():
        result["title"] = "New Task"

    return result


def process_task_command(user_message: str, user_id: int, mock_tasks: List[Dict] = None) -> Tuple[str, List[Dict]]:
    """Process natural language commands for task management"""
    if mock_tasks is None:
        mock_tasks = []

    user_msg_lower = user_message.lower().strip()

    # Check for greeting
    if any(greeting in user_msg_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
        return "Hello! I'm your AI assistant. How can I help you manage your tasks today?", []

    # Check for time/weather related queries
    if 'time' in user_msg_lower and 'what time' in user_msg_lower:
        current_time = datetime.now().strftime('%H:%M:%S')
        return f"The current time is {current_time}. How can I help with your tasks?", []
    elif 'date' in user_msg_lower and ('what date' in user_msg_lower or 'today\'s date' in user_msg_lower):
        current_date = datetime.now().strftime('%Y-%m-%d')
        return f"Today's date is {current_date}. What task would you like to manage?", []

    # Determine intent
    if any(cmd in user_msg_lower for cmd in ['list', 'show', 'display', 'view', 'get', 'fetch']):
        # List tasks
        if 'urgent' in user_msg_lower or 'high priority' in user_msg_lower:
            urgent_tasks = [t for t in mock_tasks if t.get('priority', '').lower() in ['urgent', 'high']]
            if urgent_tasks:
                task_list = "\n".join([f"- {t['title']} (Priority: {t.get('priority', 'medium')})" for t in urgent_tasks])
                response = f"Here are your urgent/high priority tasks:\n{task_list}"
            else:
                response = "You don't have any urgent or high priority tasks right now."
            return response, [{"name": "list_tasks", "arguments": {"priority": "urgent"}}]

        elif 'completed' in user_msg_lower:
            completed_tasks = [t for t in mock_tasks if t.get('completed', False)]
            if completed_tasks:
                task_list = "\n".join([f"- {t['title']}" for t in completed_tasks])
                response = f"Here are your completed tasks:\n{task_list}"
            else:
                response = "You don't have any completed tasks yet."
            return response, [{"name": "list_tasks", "arguments": {"completed": True}}]

        elif 'pending' in user_msg_lower or 'not done' in user_msg_lower:
            pending_tasks = [t for t in mock_tasks if not t.get('completed', False)]
            if pending_tasks:
                task_list = "\n".join([f"- {t['title']} (Priority: {t.get('priority', 'medium')})" for t in pending_tasks])
                response = f"You have {len(pending_tasks)} pending tasks:\n{task_list}"
            else:
                response = "You don't have any pending tasks."
            return response, [{"name": "list_tasks", "arguments": {"completed": False}}]

        else:
            if mock_tasks:
                task_list = "\n".join([f"- {t['title']} (Priority: {t.get('priority', 'medium')})" for t in mock_tasks])
                response = f"You have {len(mock_tasks)} tasks:\n{task_list}"
            else:
                response = "You don't have any tasks yet."
            return response, [{"name": "list_tasks", "arguments": {}}]

    elif any(cmd in user_msg_lower for cmd in ['add', 'create', 'new', 'make', 'build']) and any(word in user_msg_lower for word in ['task', 'todo', 'item', 'to-do']):
        # Add task
        task_details = extract_task_details(user_message)

        # Build response
        response_parts = [f"I've created a task: '{task_details['title']}'"]

        if task_details['priority'] != 'medium':
            response_parts.append(f"with {task_details['priority']} priority")

        if task_details['due_date']:
            response_parts.append(f"due on {task_details['due_date']}")

        if task_details['recurring']:
            response_parts.append(f"recurring {task_details['recurrence_pattern']}")

        if task_details['tags']:
            response_parts.append(f"with tags {task_details['tags']}")

        response = " ".join(response_parts) + "."

        # Create tool call
        tool_args = {
            "title": task_details['title'],
            "description": "",
            "priority": task_details['priority'],
            "user_id": str(user_id)  # Ensure user_id is string
        }

        if task_details['due_date']:
            tool_args["due_date"] = task_details['due_date']
        if task_details['tags']:
            tool_args["tags"] = task_details['tags']
        if task_details['recurring']:
            tool_args["recurring"] = True
            tool_args["recurrence_pattern"] = task_details['recurrence_pattern']

        return response, [{"name": "add_task", "arguments": tool_args}]

    elif any(cmd in user_msg_lower for cmd in ['update', 'change', 'modify', 'edit']) or any(word in user_msg_lower for word in ['complete', 'done', 'finish', 'mark']):
        # Handle updates and completions
        # Look for task references in the message
        task_number_match = re.search(r'task\s+(\d+)', user_msg_lower)
        if task_number_match:
            task_id = int(task_number_match.group(1))

            if any(word in user_msg_lower for word in ['complete', 'done', 'finish', 'mark']):
                return f"I've marked task {task_id} as complete.", [{"name": "complete_task", "arguments": {"id": task_id, "user_id": str(user_id)}}]
            else:
                # For updates, extract what needs to be updated
                response = f"What would you like to update for task {task_id}? Please specify the changes."
                return response, []
        else:
            if any(word in user_msg_lower for word in ['complete', 'done', 'finish', 'mark']):
                response = "Which task would you like to mark as complete? Please specify the task number or name."
                return response, []
            else:
                response = "Which task would you like to update? Please specify the task number or name and what changes to make."
                return response, []

    elif any(cmd in user_msg_lower for cmd in ['delete', 'remove', 'cancel']):
        # Delete task
        task_number_match = re.search(r'task\s+(\d+)', user_msg_lower)
        if task_number_match:
            task_id = int(task_number_match.group(1))
            return f"I've deleted task {task_id}.", [{"name": "delete_task", "arguments": {"id": task_id, "user_id": str(user_id)}}]
        else:
            response = "Which task would you like to delete? Please specify the task number or name."
            return response, []

    else:
        # Default response for unrecognized commands
        response = f"I understood you want to do something with tasks. Could you please be more specific? For example: 'Add a task to buy groceries' or 'Show me my tasks'."
        return response, []


def process_chat_message(user_message: str, user_id: int, conversation_id: int = None, mock_tasks: List[Dict] = None) -> Dict[str, Any]:
    """Process a chat message and return AI response with proper tool calls"""
    global next_conv_id

    # Create new conversation if none provided
    if conversation_id is None:
        conversation_id = next_conv_id
        next_conv_id += 1

        conversation = {
            "id": conversation_id,
            "title": f"Chat with User {user_id}",
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat()
        }

        conversations_db[conversation_id] = conversation
        messages_db[conversation_id] = []

    # Add user message
    user_msg = add_message_to_conversation(conversation_id, user_message, "user", user_id)

    # Process message with enhanced logic
    ai_response, tool_calls = process_task_command(user_message, user_id, mock_tasks)

    # Add AI response
    ai_msg = add_message_to_conversation(conversation_id, ai_response, "assistant", user_id)

    return {
        "conversation_id": conversation_id,
        "response": ai_response,
        "tool_calls": tool_calls,
        "user_message": user_msg,
        "ai_response": ai_msg
    }


def get_available_commands():
    """Return list of available commands for the chatbot"""
    return [
        "Add a task to [task description]",
        "Create a [priority] task to [task description]",
        "Show me my tasks",
        "List [priority] tasks (e.g., urgent, high, low)",
        "Show completed tasks",
        "Show pending tasks",
        "Complete task [number]",
        "Mark task [number] as done",
        "Update task [number] to [changes]",
        "Delete task [number]",
        "Add tags [tag1, tag2] to task [number]",
        "Set due date for task [number] to [date]",
        "Create recurring task [description] [frequency]"
    ]
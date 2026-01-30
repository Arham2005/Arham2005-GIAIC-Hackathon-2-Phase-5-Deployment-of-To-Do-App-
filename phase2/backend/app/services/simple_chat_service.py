"""
Simple chat service that simulates AI responses without complex models
This avoids the model conflicts while providing basic chat functionality
"""
import json
from datetime import datetime
from typing import Dict, List, Any

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

def simulate_ai_response(user_message: str, mock_tasks: List[Dict] = None) -> tuple[str, List[Dict]]:
    """Simulate AI response based on user message and return potential tool calls"""
    if mock_tasks is None:
        mock_tasks = []  # In a real implementation, this would come from DB

    user_msg_lower = user_message.lower().strip()

    # Handle natural language commands for tasks
    if any(cmd in user_msg_lower for cmd in ['list ', 'show ', 'display ', 'give me', 'get ']) and any(word in user_msg_lower for word in ['task', 'tasks']):
        if 'urgent' in user_msg_lower or 'high priority' in user_msg_lower or 'important' in user_msg_lower:
            urgent_tasks = [task for task in mock_tasks if task.get('priority', '').lower() in ['urgent', 'high']]
            if urgent_tasks:
                task_list = "\n".join([f"- {task['title']} (Priority: {task.get('priority', 'medium')})" for task in urgent_tasks])
                response = f"I found {len(urgent_tasks)} urgent/high priority tasks:\n{task_list}"
            else:
                response = "You don't have any urgent/high priority tasks right now."
            return response, [{"name": "list_tasks", "arguments": {"priority": "urgent"}}]

        elif 'completed' in user_msg_lower:
            completed_tasks = [task for task in mock_tasks if task.get('completed', False)]
            if completed_tasks:
                task_list = "\n".join([f"- {task['title']}" for task in completed_tasks])
                response = f"You have completed {len(completed_tasks)} tasks:\n{task_list}"
            else:
                response = "You don't have any completed tasks yet."
            return response, [{"name": "list_tasks", "arguments": {"completed": True}}]

        elif 'pending' in user_msg_lower or 'not done' in user_msg_lower:
            pending_tasks = [task for task in mock_tasks if not task.get('completed', False)]
            if pending_tasks:
                task_list = "\n".join([f"- {task['title']} (Priority: {task.get('priority', 'medium')})" for task in pending_tasks])
                response = f"You have {len(pending_tasks)} pending tasks:\n{task_list}"
            else:
                response = "You don't have any pending tasks."
            return response, [{"name": "list_tasks", "arguments": {"completed": False}}]

        else:
            if mock_tasks:
                task_list = "\n".join([f"- {task['title']} (Priority: {task.get('priority', 'medium')})" for task in mock_tasks])
                response = f"You have {len(mock_tasks)} tasks:\n{task_list}"
            else:
                response = "You don't have any tasks yet."
            return response, [{"name": "list_tasks", "arguments": {}}]

    elif any(cmd in user_msg_lower for cmd in ['add ', 'create ', 'make ', 'new ']) and any(word in user_msg_lower for word in ['task', 'todo']):
        # Extract task details from natural language
        import re
        title_match = re.search(r"(?:add|create|make|new)\s+(?:a\s+)?(?:task|todo|to-do)\s+(.+?)(?:\s+with\s+prio|\.|$)", user_msg_lower)
        if title_match:
            task_title = title_match.group(1).strip()
        else:
            task_title = "New task from chat"

        # Check for priority
        priority = 'medium'
        if any(word in user_msg_lower for word in ['urgent', 'critical', 'immediate']):
            priority = 'urgent'
        elif any(word in user_msg_lower for word in ['high', 'important']):
            priority = 'high'
        elif any(word in user_msg_lower for word in ['low', 'minor']):
            priority = 'low'

        response = f"I've created a task: '{task_title}' with {priority} priority."
        return response, [{"name": "add_task", "arguments": {"title": task_title, "priority": priority}}]

    elif 'complete' in user_msg_lower or 'done' in user_msg_lower or 'finish' in user_msg_lower:
        # Look for task to complete
        task_to_complete = None
        for task in mock_tasks:
            if task['title'].lower() in user_msg_lower or any(word in user_msg_lower.split() for word in task['title'].lower().split()):
                task_to_complete = task['id']
                break

        if task_to_complete:
            response = f"I've marked the task '{mock_tasks[0]['title'] if mock_tasks else 'unknown'}' as complete."
            return response, [{"name": "complete_task", "arguments": {"id": task_to_complete}}]
        else:
            response = "Which task would you like to mark as complete?"
            return response, []

    elif any(word in user_msg_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your AI assistant. How can I help you with your tasks today?", []
    elif any(word in user_msg_lower for word in ['task', 'add', 'create']):
        return "I can help you manage tasks! You can ask me to add, update, or check your tasks.", []
    elif any(word in user_msg_lower for word in ['due', 'date', 'deadline']):
        return "I can help you manage due dates for your tasks. Would you like to set or check due dates?", []
    elif any(word in user_msg_lower for word in ['priority', 'important', 'urgent']):
        return "I can help you set priorities for your tasks. What priority level would you like to set?", []
    elif any(word in user_msg_lower for word in ['help', 'assist', 'support']):
        return "I'm here to help! You can ask me to list tasks, add tasks, mark tasks as complete, or check priorities.", []
    elif 'weather' in user_msg_lower:
        return "I can't check the weather, but I can help you manage tasks related to weather!", []
    elif 'time' in user_msg_lower:
        return f"The current time is {datetime.now().strftime('%H:%M:%S')} but I can help you with time-sensitive tasks!", []
    else:
        response = f"I understand you said: '{user_message}'. I can help you manage your tasks. Try saying 'list urgent tasks' or 'add a new task'."
        return response, []

def process_chat_message(user_message: str, user_id: int, conversation_id: int = None, mock_tasks: List[Dict] = None) -> Dict[str, Any]:
    """Process a chat message and return AI response"""
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

    # Simulate AI response with potential tool calls
    ai_response, tool_calls = simulate_ai_response(user_message, mock_tasks)

    # Add AI response
    ai_msg = add_message_to_conversation(conversation_id, ai_response, "assistant", user_id)

    return {
        "conversation_id": conversation_id,
        "response": ai_response,
        "tool_calls": tool_calls,
        "user_message": user_msg,
        "ai_response": ai_msg
    }
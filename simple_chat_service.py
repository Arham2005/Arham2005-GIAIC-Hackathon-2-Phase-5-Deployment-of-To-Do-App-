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

def simulate_ai_response(user_message: str) -> str:
    """Simulate AI response based on user message"""
    user_msg_lower = user_message.lower()

    if any(word in user_msg_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm your AI assistant. How can I help you with your tasks today?"
    elif any(word in user_msg_lower for word in ['task', 'add', 'create']):
        return "I can help you manage tasks! You can ask me to add, update, or check your tasks."
    elif any(word in user_msg_lower for word in ['complete', 'done', 'finish']):
        return "Great! I can help mark tasks as complete. Which task would you like to mark as done?"
    elif any(word in user_msg_lower for word in ['due', 'date', 'deadline']):
        return "I can help you manage due dates for your tasks. Would you like to set or check due dates?"
    elif any(word in user_msg_lower for word in ['priority', 'important', 'urgent']):
        return "I can help you set priorities for your tasks. What priority level would you like to set?"
    elif any(word in user_msg_lower for word in ['help', 'assist', 'support']):
        return "I'm here to help! You can ask me to add tasks, update task status, set due dates, or manage priorities."
    else:
        return f"I understand you said: '{user_message}'. I'm your AI assistant and can help with managing your tasks. Try asking me to add a task or check your task list!"

def process_chat_message(user_message: str, user_id: int, conversation_id: int = None) -> Dict[str, Any]:
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

    # Simulate AI response
    ai_response = simulate_ai_response(user_message)

    # Add AI response
    ai_msg = add_message_to_conversation(conversation_id, ai_response, "assistant", user_id)

    return {
        "conversation_id": conversation_id,
        "response": ai_response,
        "tool_calls": [],  # No actual tool calls in simulation
        "user_message": user_msg,
        "ai_response": ai_msg
    }
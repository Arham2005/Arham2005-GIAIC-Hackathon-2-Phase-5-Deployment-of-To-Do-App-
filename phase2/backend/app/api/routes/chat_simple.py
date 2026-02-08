"""Simple chat API router for Phase 2 backend"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ...api.deps import get_db, get_current_user
from shared.models.user import User
from ...services.task_service import create_task, get_tasks, update_task, delete_task, complete_task
from ...services.simple_chat_service import process_chat_message, create_conversation, get_conversation_messages

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict]

class ConversationCreate(BaseModel):
    title: str

class MessageCreate(BaseModel):
    content: str

class Message(BaseModel):
    id: int
    content: str
    role: str
    conversation_id: int
    created_at: str

class Conversation(BaseModel):
    id: int
    title: str
    created_at: str

@router.post("/start")
def start_conversation(
    conv_data: ConversationCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Start a new conversation
    """
    conversation = create_conversation(current_user.id, conv_data.title)
    return conversation

@router.post("/{user_id}/chat")
def chat_endpoint(
    user_id: int,
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Chat endpoint following the API specification
    POST /api/{user_id}/chat - Send message & get AI response
    """
    # Verify that the user matches the current authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's chat"
        )

    # Get user's tasks to provide context for the AI
    from ...services.task_service import get_tasks
    user_tasks = get_tasks(db, current_user.id, skip=0, limit=100)

    # Process the message with simulated AI and get response
    result = process_chat_message(
        user_message=chat_request.message,
        user_id=current_user.id,
        conversation_id=chat_request.conversation_id,
        mock_tasks=[{
            "id": task.id,
            "title": task.title,
            "description": getattr(task, 'description', ''),
            "completed": getattr(task, 'completed', False),
            "priority": getattr(task, 'priority', 'medium'),
            "due_date": getattr(task, 'due_date', None),
            "created_at": getattr(task, 'created_at', None)
        } for task in user_tasks] if user_tasks else []
    )

    # Execute tool calls if any
    from ...services.task_service import create_task, get_task_by_id, update_task, complete_task, delete_task
    from shared.models.task import TaskCreate, TaskUpdate

    for tool_call in result.get("tool_calls", []):
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("arguments", {})

        # Ensure user_id is always set to the current user's ID
        tool_args["user_id"] = str(current_user.id)

        try:
            if tool_name == "add_task":
                # Prepare task data
                task_data = TaskCreate(
                    title=tool_args.get("title", "Untitled Task"),
                    description=tool_args.get("description", ""),
                    priority=tool_args.get("priority", "medium"),
                    tags=tool_args.get("tags", []),
                    due_date=tool_args.get("due_date"),
                    recurring=tool_args.get("recurring", False),
                    recurrence_pattern=tool_args.get("recurrence_pattern"),
                    parent_task_id=tool_args.get("parent_task_id")
                )

                # Execute the create task operation
                created_task = create_task(db, task_data, current_user.id)

            elif tool_name == "list_tasks":
                # This is just information retrieval, no DB write needed
                pass

            elif tool_name == "complete_task":
                task_id = int(tool_args.get("id"))
                complete_task(db, task_id, current_user.id)

            elif tool_name == "update_task":
                task_id = int(tool_args.get("id"))
                task_update = TaskUpdate(
                    title=tool_args.get("title"),
                    description=tool_args.get("description"),
                    priority=tool_args.get("priority"),
                    tags=tool_args.get("tags"),
                    completed=tool_args.get("completed"),
                    due_date=tool_args.get("due_date"),
                    recurring=tool_args.get("recurring"),
                    recurrence_pattern=tool_args.get("recurrence_pattern"),
                    parent_task_id=tool_args.get("parent_task_id"),
                    reminder_sent=tool_args.get("reminder_sent")
                )
                update_task(db, task_id, task_update, current_user.id)

            elif tool_name == "delete_task":
                task_id = int(tool_args.get("id"))
                delete_task(db, task_id, current_user.id)

        except Exception as e:
            # Log the error but continue processing other tool calls
            print(f"Error executing tool {tool_name}: {str(e)}")
            continue

    return ChatResponse(
        conversation_id=result["conversation_id"],
        response=result["response"],
        tool_calls=result.get("tool_calls", [])  # Return for frontend feedback
    )

@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user)
):
    """
    Get conversation history
    """
    # For simplicity in this simulation, we don't check ownership
    # In a real implementation, we would verify the conversation belongs to the user
    messages = get_conversation_messages(conversation_id)

    return {
        "conversation": {
            "id": conversation_id,
            "title": f"Conversation {conversation_id}",
            "created_at": datetime.utcnow().isoformat()
        },
        "messages": messages
    }

# Legacy endpoint for compatibility
@router.post("/{conversation_id}/message")
def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Legacy endpoint for sending a message in a conversation and getting AI response
    """
    # Process the message with simulated AI and get response
    result = process_chat_message(
        user_message=message_data.content,
        user_id=current_user.id,
        conversation_id=conversation_id
    )

    return {
        "user_message": result["user_message"],
        "ai_response": result["ai_response"],
        "conversation_id": result["conversation_id"]
    }
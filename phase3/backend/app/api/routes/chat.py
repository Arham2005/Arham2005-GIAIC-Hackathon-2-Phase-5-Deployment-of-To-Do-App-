from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
from ...models.conversation import Conversation, ConversationCreate
from ...models.message import Message, MessageCreate
from ...services.conversation_service import create_conversation, get_conversation_by_id, add_message_to_conversation, get_messages_for_conversation
from ...ai.runner import run_chat_completion
from phase2.backend.app.api.deps import get_db, get_current_user
from shared.models.user import User
from pydantic import BaseModel


router = APIRouter()


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict]


@router.post("/start")
def start_conversation(
    conv_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Start a new conversation
    """
    conversation_data = conv_data.dict()
    conversation = create_conversation(db, conversation_data, current_user.id)
    return conversation


@router.post("/{user_id}/chat")
def chat_endpoint(
    user_id: int,
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Chat endpoint following the new API specification
    POST /api/{user_id}/chat - Send message & get AI response
    """
    # Verify that the user matches the current authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's chat"
        )

    # If no conversation_id is provided, create a new one
    conversation_id = chat_request.conversation_id
    if not conversation_id:
        # Create a new conversation
        conv_data = ConversationCreate(title=f"Chat {current_user.email}")
        conversation = create_conversation(db, conv_data.dict(), current_user.id)
        conversation_id = conversation.id
    else:
        # Verify that the conversation belongs to the current user
        conversation = get_conversation_by_id(db, conversation_id, current_user.id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

    # Add user message to conversation
    user_message = add_message_to_conversation(
        db,
        conversation_id=conversation_id,
        content=chat_request.message,
        role="user",
        user_id=current_user.id
    )

    # Process the message with the OpenAI agent and get response
    result = run_chat_completion(chat_request.message, user_id, db)

    # Add AI response to conversation
    ai_message = add_message_to_conversation(
        db,
        conversation_id=conversation_id,
        content=result["response"],
        role="assistant",
        user_id=current_user.id
    )

    return ChatResponse(
        conversation_id=conversation_id,
        response=result["response"],
        tool_calls=result.get("tool_calls", [])
    )


@router.post("/{conversation_id}/message")
def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Legacy endpoint for sending a message in a conversation and getting AI response
    """
    # Verify that the conversation belongs to the current user
    conversation = get_conversation_by_id(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Add user message to conversation
    user_message = add_message_to_conversation(
        db,
        conversation_id=conversation_id,
        content=message_data.content,
        role="user",
        user_id=current_user.id
    )

    # Process the message with the OpenAI agent and get response
    result = run_chat_completion(message_data.content, current_user.id, db)

    # Add AI response to conversation
    ai_message = add_message_to_conversation(
        db,
        conversation_id=conversation_id,
        content=result["response"],
        role="assistant",
        user_id=current_user.id
    )

    return {
        "user_message": user_message,
        "ai_response": ai_message,
        "conversation_id": conversation_id
    }


@router.get("/{conversation_id}")
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get conversation history
    """
    conversation = get_conversation_by_id(db, conversation_id, current_user.id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    # Get all messages for this conversation
    messages = get_messages_for_conversation(db, conversation_id, current_user.id)

    return {
        "conversation": conversation,
        "messages": messages
    }
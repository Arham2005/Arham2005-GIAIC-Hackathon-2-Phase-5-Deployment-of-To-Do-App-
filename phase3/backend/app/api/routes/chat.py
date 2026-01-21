from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ...models.conversation import Conversation, ConversationCreate
from ...models.message import Message, MessageCreate
from ...services.conversation_service import create_conversation, get_conversation_by_id, add_message_to_conversation, get_messages_for_conversation
from ...ai.agent import process_user_message
from phase2.backend.app.api.deps import get_db, get_current_user
from shared.models.user import User

router = APIRouter()


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


@router.post("/{conversation_id}/message")
def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Send a message in a conversation and get AI response
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

    # Process the message with the AI agent and get response
    ai_response_content = process_user_message(message_data.content, current_user.id, db)

    # Add AI response to conversation
    ai_message = add_message_to_conversation(
        db,
        conversation_id=conversation_id,
        content=ai_response_content,
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
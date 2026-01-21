from typing import List, Optional
from sqlmodel import Session, select
from sqlalchemy import and_
from ..models.conversation import Conversation
from ..models.message import Message


def create_conversation(db: Session, conversation_data: dict, user_id: int) -> Conversation:
    db_conversation = Conversation(**conversation_data)
    db_conversation.user_id = user_id
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_conversation_by_id(db: Session, conversation_id: int, user_id: int) -> Optional[Conversation]:
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    return db.exec(statement).first()


def get_conversations_for_user(db: Session, user_id: int) -> List[Conversation]:
    statement = select(Conversation).where(Conversation.user_id == user_id)
    return db.exec(statement).all()


def add_message_to_conversation(
    db: Session,
    conversation_id: int,
    content: str,
    role: str,
    user_id: int
) -> Message:
    message = Message(
        content=content,
        role=role,
        conversation_id=conversation_id,
        user_id=user_id
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages_for_conversation(db: Session, conversation_id: int, user_id: int) -> List[Message]:
    # Verify the conversation belongs to the user
    conversation = get_conversation_by_id(db, conversation_id, user_id)
    if not conversation:
        return []

    # Get messages for this conversation
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.asc())

    return db.exec(statement).all()
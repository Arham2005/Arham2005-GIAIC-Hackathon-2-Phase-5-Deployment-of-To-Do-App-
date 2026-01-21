from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from enum import Enum
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from .conversation import Conversation


class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"


class MessageBase(SQLModel):
    content: str
    role: MessageRole
    conversation_id: int


class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    role: MessageRole
    conversation_id: int = Field(foreign_key="conversation.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(SQLModel):
    content: str


class MessageRead(MessageBase):
    id: int
    created_at: datetime
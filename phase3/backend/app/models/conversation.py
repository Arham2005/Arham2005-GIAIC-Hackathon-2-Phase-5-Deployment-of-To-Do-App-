from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .message import Message


class ConversationBase(SQLModel):
    title: str
    user_id: int


class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    user_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: list["Message"] = Relationship(back_populates="conversation", cascade_delete=True)


class ConversationCreate(SQLModel):
    title: str


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
    messages: list["Message"] = []
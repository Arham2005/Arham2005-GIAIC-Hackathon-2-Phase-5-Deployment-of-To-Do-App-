from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routes from Phase 2 that use shared models consistently
from phase2.backend.app.api.routes.auth import router as auth_router
from phase2.backend.app.api.routes.tasks import router as task_router

# Import chat route that's adapted to use shared models
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional
import json

# Use shared models
from shared.models.user import User
from phase2.backend.app.api.deps import get_db, get_current_user
from phase3.backend.app.ai.runner import run_chat_completion

# Create a simple chat router that doesn't import conflicting models
chat_router = APIRouter()

class ChatRequest:
    def __init__(self):
        self.conversation_id: Optional[int] = None
        self.message: str = ""

class ChatResponse:
    def __init__(self):
        self.conversation_id: int = 0
        self.response: str = ""
        self.tool_calls: List[dict] = []


@chat_router.post("/start")
def start_conversation():
    """
    Start a new conversation
    """
    return {"conversation_id": 1, "title": "New Conversation", "started": True}


@chat_router.post("/{user_id}/chat")
def chat_endpoint(
    user_id: int,
    request_data: dict,  # Use dict instead of Pydantic model to avoid import conflicts
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Chat endpoint following the new API specification
    POST /api/{user_id}/chat - Send message & get AI response
    """
    # Extract data from the dict
    message = request_data.get('message', '')
    conversation_id = request_data.get('conversation_id')

    # Verify that the user matches the current authenticated user
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's chat"
        )

    # Process the message with the OpenAI agent and get response
    result = run_chat_completion(message, user_id, db)

    return {
        "conversation_id": conversation_id or 1,
        "response": result["response"],
        "tool_calls": result.get("tool_calls", [])
    }


# Main app
app = FastAPI(title="Todo AI Chat API", version="1.0.0")

# CORS middleware - in production, configure properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes using only shared models
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo AI Chat API v1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
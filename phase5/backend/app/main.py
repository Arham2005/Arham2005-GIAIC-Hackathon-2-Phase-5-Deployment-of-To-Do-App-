from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from phase2.backend.app.api.routes.auth import router as auth_router
from phase5.backend.app.api.routes.tasks import router as task_router
# Handle the chat router import carefully to avoid table conflicts
try:
    from phase3.backend.app.api.routes.chat import router as chat_router
except Exception as e:
    print(f"Warning: Could not import Phase 3 chat router: {e}")
    print("Falling back to simple chat router...")
    try:
        from phase2.backend.app.api.routes.chat_simple import router as chat_router
    except Exception as e2:
        print(f"Warning: Could not import simple chat router either: {e2}")
        # Create a dummy router if both fail
        from fastapi import APIRouter
        chat_router = APIRouter()

        @chat_router.get("/")
        def chat_unavailable():
            return {"error": "Chat functionality not available"}

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Todo AI Chat API - Phase 5 Advanced Features", version="2.0.0")

# CORS middleware - in production, configure properly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(task_router, prefix="/tasks", tags=["tasks"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo AI Chat API - Phase 5 Advanced Features v2.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "features": ["advanced_tasks", "recurring", "due_dates", "priorities", "tags", "search", "filters", "kafka", "dapr"]}
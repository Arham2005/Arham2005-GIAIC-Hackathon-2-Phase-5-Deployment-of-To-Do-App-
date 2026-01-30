from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import chat
from .api.routes.tasks import router as task_router
from phase2.backend.app.api.routes.auth import router as auth_router
import os

app = FastAPI(title="Todo AI Chat API", version="1.0.0")

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
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo AI Chat API v1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
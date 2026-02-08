#!/usr/bin/env python3
"""
Unified Backend for All Phases
==============================

This file serves as a single entry point to run all phases of the application:
- Phase 2: Full-Stack Multi-User Web Application
- Phase 3: AI-Powered Todo Chat System
- Phase 5: Advanced Cloud Features (Recurring tasks, due dates, priorities, etc.)

The unified backend combines all functionality into one cohesive application
allowing seamless navigation between features from the frontend.
"""

import sys
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_unified_app():
    """Create the unified FastAPI application with all phase features."""

    app = FastAPI(
        title="Unified Todo AI Chat Platform - All Phases Combined",
        version="3.0.0",
        description="Single backend serving Phase 2 (Web App), Phase 3 (Chatbot), and Phase 5 (Advanced Features)"
    )

    # CORS middleware - configure properly in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import and register routers with careful error handling to avoid model conflicts
    try:
        # Phase 2: Core authentication and basic tasks
        from phase2.backend.app.api.routes.auth import router as auth_router
        from phase2.backend.app.api.routes.tasks import router as basic_task_router

        app.include_router(auth_router, prefix="/auth", tags=["authentication"])
        app.include_router(basic_task_router, prefix="/basic-tasks", tags=["basic-tasks"])

        print("[OK] Phase 2 routers loaded successfully")
    except Exception as e:
        print(f"[WARN] Phase 2 routers failed to load: {e}")

    try:
        # Phase 5: Advanced task features (loaded separately to avoid conflicts with Phase 3)
        from phase5.backend.app.api.routes.tasks import router as advanced_task_router
        app.include_router(advanced_task_router, prefix="/tasks", tags=["advanced-tasks"])
        print("[OK] Phase 5 advanced tasks router loaded successfully")
    except Exception as e:
        print(f"[WARN] Phase 5 advanced tasks router failed to load: {e}")
        # Fallback to basic tasks if advanced tasks fail
        try:
            from phase2.backend.app.api.routes.tasks import router as basic_task_router
            app.include_router(basic_task_router, prefix="/tasks", tags=["tasks"])
            print("[OK] Basic tasks router loaded as fallback for advanced tasks")
        except Exception as e2:
            print(f"[WARN] Basic tasks router also failed: {e2}")

    try:
        # Phase 3: AI-powered chat system (with fallback)
        from phase3.backend.app.api.routes.chat import router as chat_router
        app.include_router(chat_router, prefix="/chat", tags=["chat"])
        print("[OK] Phase 3 chat router loaded successfully")
    except Exception as e:
        print(f"[WARN] Phase 3 chat router failed to load: {e}")
        print("   Falling back to simple chat...")
        try:
            from phase2.backend.app.api.routes.chat_simple import router as chat_simple_router
            app.include_router(chat_simple_router, prefix="/simple-chat", tags=["simple-chat"])
            print("[OK] Simple chat router loaded as fallback")
        except Exception as e2:
            print(f"[WARN] Simple chat router also failed: {e2}")

    @app.get("/")
    def read_root():
        return {
            "message": "Unified Todo AI Chat Platform - All Phases Active",
            "version": "3.0.0",
            "features": [
                "Phase 2: Multi-user web application with authentication",
                "Phase 3: AI-powered chat system with MCP tools",
                "Phase 5: Advanced features (recurring tasks, due dates, priorities, tags, etc.)",
                "Kafka event streaming",
                "Dapr integration for cloud-native deployment"
            ]
        }

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "active_phases": ["phase2", "phase3", "phase5"],
            "features": [
                "authentication",
                "basic_tasks",
                "advanced_tasks",
                "ai_chat",
                "recurring_tasks",
                "due_dates",
                "priorities",
                "tags",
                "search_filters",
                "kafka_streaming",
                "dapr_integration"
            ]
        }

    @app.get("/phases-info")
    def phases_info():
        return {
            "phase2": {
                "description": "Full-Stack Multi-User Web Application",
                "endpoints": ["/auth/*", "/basic-tasks/*"],
                "features": ["JWT authentication", "User isolation", "Basic CRUD operations"]
            },
            "phase3": {
                "description": "AI-Powered Todo Chat System",
                "endpoints": ["/chat/*"],
                "features": ["Natural language processing", "MCP tools", "Conversational AI"]
            },
            "phase5": {
                "description": "Advanced Cloud Features",
                "endpoints": ["/tasks/*"],
                "features": ["Recurring tasks", "Due dates", "Priorities", "Tags", "Advanced search", "Kafka", "Dapr"]
            }
        }

    return app

def init_database():
    """Initialize the database with required tables for all phases."""
    print("Initializing database with all phase schemas...")

    try:
        # Initialize with Phase 5 advanced schema (includes all features)
        from phase5.backend.app.database import create_tables
        create_tables()
        print("Database initialized successfully with advanced features!")
    except ImportError as e:
        print(f"Advanced database initialization failed: {e}")
        print("Falling back to basic database initialization...")

        try:
            # Fallback to shared database schema
            from shared.db.base import create_tables
            create_tables()
            print("Database initialized with basic schema!")
        except ImportError:
            print("Could not initialize database - please check your setup")

def main():
    """Main entry point to run the unified backend."""
    print("=" * 70)
    print(" unified todo ai chat platform ")
    print(" all phases combined backend ")
    print("=" * 70)
    print("Features available:")
    print("- Phase 2: Multi-user web application with authentication")
    print("- Phase 3: AI-powered chat system with MCP tools")
    print("- Phase 5: Advanced features (recurring tasks, due dates, priorities, etc.)")
    print("=" * 70)

    # Initialize database
    init_database()

    # Create the unified application
    app = create_unified_app()

    print("\nStarting unified backend server...")
    print("Access the application at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    print("Phase info: http://localhost:8000/phases-info")
    print("-" * 60)

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
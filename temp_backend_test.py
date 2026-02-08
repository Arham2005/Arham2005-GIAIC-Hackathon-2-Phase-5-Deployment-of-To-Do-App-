#!/usr/bin/env python3
"""
Temporary backend for testing the fixes
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
    """Create the unified FastAPI application with all phase features, avoiding model conflicts."""

    app = FastAPI(
        title="Unified Todo AI Chat Platform - Test Version",
        version="3.4.0",
        description="Test version with fixed tool execution and serialization"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import and register routers
    try:
        # Phase 2: Core authentication and basic tasks
        from phase2.backend.app.api.routes.auth import router as auth_router
        from phase2.backend.app.api.routes.tasks import router as basic_task_router

        app.include_router(auth_router, prefix="/auth", tags=["authentication"])
        app.include_router(basic_task_router, prefix="/basic-tasks", tags=["basic-tasks"])

        print("[OK] Phase 2 routers loaded successfully")
    except Exception as e:
        print(f"[ERROR] Phase 2 routers failed to load: {e}")
        raise

    # Load Phase 5 advanced tasks
    try:
        from phase5.backend.app.api.routes.tasks import router as advanced_task_router
        app.include_router(advanced_task_router, prefix="/tasks", tags=["advanced-tasks"])
        print("[OK] Phase 5 advanced tasks router loaded successfully")
    except Exception as e:
        print(f"[WARN] Phase 5 advanced tasks router failed to load: {e}")
        try:
            from phase2.backend.app.api.routes.tasks import router as basic_task_router
            app.include_router(basic_task_router, prefix="/tasks", tags=["tasks"])
            print("[OK] Basic tasks router loaded as fallback for advanced tasks")
        except Exception as e2:
            print(f"[WARN] Basic tasks router also failed: {e2}")

    # Load Phase 3 chat with fix
    try:
        from phase2.backend.app.api.routes.chat_simple import router as chat_simple_router
        app.include_router(chat_simple_router, prefix="/chat", tags=["chat"])
        print("[OK] Phase 3 simple chat router loaded successfully")
    except Exception as e:
        print(f"[ERROR] Phase 3 chat router failed to load: {e}")

    @app.get("/")
    def read_root():
        return {
            "message": "Unified Todo AI Chat Platform - Test Version",
            "version": "3.4.0",
            "status": "running with fixed tool execution"
        }

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "active_features": ["authentication", "basic_tasks", "ai_chat", "advanced_tasks"]
        }

    return app


def init_database():
    """Initialize the database with required tables."""
    print("Initializing database with all phase schemas...")

    try:
        from phase5.backend.app.database import create_tables
        create_tables()
        print("Database initialized successfully with advanced features!")
    except ImportError as e:
        print(f"Advanced database initialization failed: {e}")
        print("Falling back to basic database initialization...")

        try:
            from shared.db.base import create_tables
            create_tables()
            print("Database initialized with basic schema!")
        except ImportError:
            print("Could not initialize database - please check your setup")


def main():
    """Main entry point to run the test backend."""
    print("=" * 70)
    print(" unified todo ai chat platform (test version) ")
    print(" with fixed tool execution and serialization ")
    print("=" * 70)
    print("Features available:")
    print("- Phase 2: Multi-user web application with authentication")
    print("- Phase 3: AI-powered chat system with fixed tool execution")
    print("- Phase 5: Advanced features")
    print("=" * 70)

    # Initialize database
    init_database()

    # Create the unified application
    app = create_unified_app()

    print("\nStarting test backend server on port 8001...")
    print("Access the application at: http://localhost:8001")
    print("-" * 60)

    # Run the server on port 8001 to avoid conflict
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)


if __name__ == "__main__":
    main()
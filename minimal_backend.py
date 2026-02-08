#!/usr/bin/env python3
"""
Minimal Backend for Phase 2 Only
================================

This backend only includes Phase 2 functionality to avoid model conflicts.
It provides authentication and basic task management without the advanced features
that are causing relationship conflicts.
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

def create_minimal_app():
    """Create a minimal FastAPI application with only stable Phase 2 features."""

    app = FastAPI(
        title="Minimal Todo Platform - Phase 2 Only",
        version="1.0.0",
        description="Minimal backend with stable authentication and basic task management"
    )

    # CORS middleware - configure properly in production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import and register only Phase 2 routers to avoid model conflicts
    try:
        # Phase 2: Core authentication and basic tasks - these are stable
        from phase2.backend.app.api.routes.auth import router as auth_router
        from phase2.backend.app.api.routes.tasks import router as basic_task_router

        app.include_router(auth_router, prefix="/auth", tags=["authentication"])
        app.include_router(basic_task_router, prefix="/tasks", tags=["tasks"])

        print("[OK] Phase 2 routers loaded successfully")
    except Exception as e:
        print(f"[ERROR] Phase 2 routers failed to load: {e}")
        raise

    @app.get("/")
    def read_root():
        return {
            "message": "Minimal Todo Platform - Phase 2 Only",
            "version": "1.0.0",
            "features": [
                "Authentication",
                "User management",
                "Basic task CRUD operations"
            ]
        }

    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "active_features": ["authentication", "basic_tasks"],
        }

    return app

def init_database():
    """Initialize the database with required tables."""
    print("Initializing database...")

    try:
        # Use shared database schema to avoid conflicts
        from shared.db.base import create_tables
        create_tables()
        print("Database initialized successfully!")
    except ImportError:
        print("Could not initialize database - please check your setup")

def main():
    """Main entry point to run the minimal backend."""
    print("=" * 60)
    print(" minimal todo platform - phase 2 only ")
    print(" stable authentication and basic tasks ")
    print("=" * 60)
    print("Features available:")
    print("- Authentication (register, login)")
    print("- Basic task management")
    print("No model conflicts - stable operation")
    print("=" * 60)

    # Initialize database
    init_database()

    # Create the minimal application
    app = create_minimal_app()

    print("\nStarting minimal backend server...")
    print("Access the application at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    print("-" * 50)

    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    main()
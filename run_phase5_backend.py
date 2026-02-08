#!/usr/bin/env python3
"""
Phase 5 Advanced Features Backend Runner
========================================

This script runs the Phase 5 backend which includes:
- Phase 2: Full-Stack Multi-User Web Application
- Phase 3: AI-Powered Todo Chat System
- Phase 5: Advanced Cloud Features (Recurring tasks, due dates, priorities, etc.)

Note: This is equivalent to the unified backend but specifically configured for Phase 5 features.
"""

import sys
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize the database with required tables for all phases."""
    print("Initializing database for Phase 5 Advanced Features with all phase schemas...")

    try:
        # Initialize Phase 5 advanced schema (includes all features)
        from phase5.backend.app.database import create_tables
        create_tables()
        print("Phase 5 database initialized successfully with advanced features!")

        # Phase 3 database.py doesn't have create_tables function, so skip it
        # Instead, ensure Phase 3 models are compatible
        try:
            from phase3.backend.app.models.conversation import Conversation
            from phase3.backend.app.models.message import Message
            print("Phase 3 chat models verified!")
        except ImportError:
            print("Phase 3 chat models not available")

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

def fix_phase5_main():
    """Ensure the Phase 5 main.py includes all necessary routes from all phases."""

    # Read the current phase5 main.py
    phase5_main_path = "phase5/backend/app/main.py"
    try:
        with open(phase5_main_path, 'r') as f:
            content = f.read()

        # Check if Phase 3 chat router is properly included
        if "from phase3.backend.app.api.routes.chat import router as chat_router" not in content:
            # Update the imports and router inclusion
            updated_content = content.replace(
                "from phase2.backend.app.api.routes.chat_simple import router as chat_router",
                "from phase3.backend.app.api.routes.chat import router as chat_router"
            )

            # Update the app.include_router line if needed
            if "app.include_router(chat_router, prefix=\"/chat\", tags=[\"chat\"])" in content:
                # Already has the right router, just make sure it's from phase3
                pass
            else:
                # Add the chat router inclusion if missing
                if "app.include_router(task_router, prefix=\"/tasks\", tags=[\"tasks\"])" in updated_content:
                    updated_content = updated_content.replace(
                        "app.include_router(task_router, prefix=\"/tasks\", tags=[\"tasks\"])",
                        "app.include_router(task_router, prefix=\"/tasks\", tags=[\"tasks\"])\napp.include_router(chat_router, prefix=\"/chat\", tags=[\"chat\"])"
                    )

            # Write the updated content back
            with open(phase5_main_path, 'w') as f:
                f.write(updated_content)

            print("Updated Phase 5 main.py to include proper Phase 3 chat router")

    except FileNotFoundError:
        print(f"Phase 5 main.py not found at {phase5_main_path}")

if __name__ == "__main__":
    print("=" * 60)
    print(" phase 5 advanced features backend ")
    print(" with all phase integration ")
    print("=" * 60)

    # Fix Phase 5 main.py to ensure proper phase integration
    fix_phase5_main()

    # Initialize database
    init_database()

    # Run the Phase 5 backend with advanced features
    print("\nStarting Phase 5 Advanced Features Backend with all phases integrated...")
    print("Access the application at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("-" * 60)

    # Try to run Phase 5 backend, but handle potential import conflicts
    try:
        import phase5.backend.app.main
        app = phase5.backend.app.main.app
        print("Using Phase 5 main app...")
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
    except Exception as e:
        print(f"Phase 5 main failed to load due to: {e}")
        print("Falling back to unified backend approach...")

        # Import and run unified app instead
        from unified_backend import create_unified_app
        app = create_unified_app()
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
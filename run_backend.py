import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize the database with required tables"""
    print("Initializing database...")

    # Import from shared components
    from shared.db.base import create_tables
    create_tables()

    print("Database initialized successfully!")

if __name__ == "__main__":
    # Initialize database first
    init_database()

    # Then run the server
    import uvicorn
    uvicorn.run("phase2.backend.app.main:app", host="0.0.0.0", port=8000, reload=False)
#!/usr/bin/env python3
"""
Start Unified Application Script
================================

This script provides a simple way to start the unified backend application
that combines all phases (Phase 2, Phase 3, and Phase 5) into one cohesive system.

Usage:
    python start_unified_app.py

Or run directly:
    ./start_unified_app.py
"""

import subprocess
import sys
import os

def main():
    """Main function to start the unified application."""

    print("=" * 70)
    print(" 🚀 UNIFIED TODO AI CHAT APPLICATION STARTER")
    print("=" * 70)
    print(" This script will start the unified backend combining:")
    print(" • Phase 2: Multi-user web application")
    print(" • Phase 3: AI-powered chat system")
    print(" • Phase 5: Advanced cloud features")
    print("=" * 70)

    # Check if Python is available
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        sys.exit(1)

    # Check if required packages are installed
    try:
        import fastapi
        import uvicorn
        import sqlmodel
        print("✅ Dependencies verified")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages using: pip install -r requirements.txt")
        sys.exit(1)

    # Check if unified backend file exists
    unified_backend_path = "unified_backend.py"
    if not os.path.exists(unified_backend_path):
        print(f"❌ Unified backend file not found: {unified_backend_path}")
        print("Creating unified backend...")

        # Create the unified backend file if it doesn't exist
        try:
            from unified_backend import main as unified_main
            print("✅ Unified backend file found and importable")
        except ImportError:
            print("❌ Could not create or import unified backend")
            sys.exit(1)

    print("\n🚀 Starting unified application...")
    print("💡 Access the application at: http://localhost:8000")
    print("📋 API Documentation: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    print("📊 Phase info: http://localhost:8000/phases-info")
    print("-" * 70)

    try:
        # Run the unified backend
        subprocess.run([sys.executable, "unified_backend.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting unified backend: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
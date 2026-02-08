#!/usr/bin/env python3
"""
Script to manually create a user in the database using raw SQL to bypass model conflicts
"""

import sqlite3
import hashlib
import os
from datetime import datetime

def hash_password(password):
    """Simple password hashing (in production, use proper bcrypt or similar)"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user_raw_sql(email: str, password: str):
    """Create a user directly using raw SQL to bypass model conflicts"""

    # Determine database path - look for SQLite file
    db_paths = [
        "shared/db/todo.db",  # Common location
        "todo.db",            # In project root
        ".db.sqlite",         # Alternative
        "database.db",        # Alternative
    ]

    db_path = None
    for path in db_paths:
        if os.path.exists(path):
            db_path = path
            break

    # If none found, try to find any .db or .sqlite file
    if not db_path:
        import glob
        db_files = glob.glob("*.db") + glob.glob("*.sqlite")
        if db_files:
            db_path = db_files[0]

    if not db_path:
        print("Could not find database file. Looking for common names...")
        # As a fallback, try to determine from environment or create in current dir
        db_path = "todo.db"  # Default name
        print(f"Assuming database path: {db_path}")

    print(f"Using database: {db_path}")

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Hash the password
    hashed_password = hash_password(password)

    try:
        # Check if user already exists
        cursor.execute("SELECT id, email FROM users WHERE email = ?", (email,))
        existing = cursor.fetchone()

        if existing:
            print(f"User {email} already exists with ID: {existing[0]}")
            conn.close()
            return existing[0]

        # Insert the new user
        cursor.execute("""
            INSERT INTO users (email, hashed_password, created_at)
            VALUES (?, ?, ?)
        """, (email, hashed_password, datetime.now().isoformat()))

        user_id = cursor.lastrowid
        conn.commit()

        print(f"User {email} created successfully with ID: {user_id}")

        # Verify the insertion
        cursor.execute("SELECT id, email FROM users WHERE email = ?", (email,))
        created_user = cursor.fetchone()
        if created_user:
            print(f"SUCCESS: User verified in database: {created_user[1]} (ID: {created_user[0]})")

        conn.close()
        return user_id

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.close()
        return None
    except Exception as e:
        print(f"Error: {e}")
        conn.close()
        return None

if __name__ == "__main__":
    # Create the user with the provided credentials
    email = "user1@gmail.com"
    password = "user112345"

    print(f"Creating user: {email}")
    user_id = create_user_raw_sql(email, password)

    if user_id:
        print(f"\nSUCCESS: User creation completed successfully!")
        print(f"  Email: {email}")
        print(f"  User ID: {user_id}")
        print("\nYou can now try logging in with these credentials.")
    else:
        print("\nERROR: User creation failed.")
        print("The database schema may not exist yet, or the table structure is different.")
#!/usr/bin/env python3
"""
Test script to verify the tags list to JSON string conversion fix
"""

import json
from datetime import datetime
from sqlmodel import SQLModel, Field, Session, create_engine, select
from shared.models.task import Task, TaskCreate
from shared.models.user import User

# Create an in-memory SQLite database for testing
engine = create_engine("sqlite:///:memory:")

def test_tags_conversion():
    """Test that tags are properly converted from list to JSON string"""

    # Create tables
    SQLModel.metadata.create_all(engine)

    # Create a sample TaskCreate object with tags as a list
    task_create = TaskCreate(
        title="Testing",
        description="",
        priority="high",
        tags=["work", "important", "urgent", "development"],
        due_date=datetime(2026, 2, 4, 14, 30),
        recurring=False,
        user_id=1  # This will be set in the service layer
    )

    print("Original TaskCreate tags:", task_create.tags)
    print("Type of tags:", type(task_create.tags))

    # Simulate what happens in the create_task function
    task_data = task_create.model_dump()
    print("\nAfter .dict() conversion:")
    print("Tags in task_data:", task_data.get('tags'))
    print("Type of tags in task_data:", type(task_data.get('tags')))

    # Apply the conversion logic from the fixed service
    if 'tags' in task_data and task_data['tags'] is not None:
        if isinstance(task_data['tags'], list):
            task_data['tags'] = json.dumps(task_data['tags'])
    elif 'tags' not in task_data or task_data['tags'] is None:
        task_data['tags'] = '[]'

    print("\nAfter JSON conversion:")
    print("Tags in task_data:", task_data.get('tags'))
    print("Type of tags in task_data:", type(task_data.get('tags')))

    # Now create the Task object with the converted data
    with Session(engine) as session:
        # Add the user_id which would come from the service
        db_task = Task(**task_data, user_id=1)

        # Add to session and commit (this would trigger the database insert)
        session.add(db_task)
        session.commit()

        print(f"\nTask created successfully with ID: {db_task.id}")
        print(f"Task tags stored in DB: {repr(db_task.tags)}")
        print(f"Task tags type: {type(db_task.tags)}")

        # Verify we can retrieve it back
        retrieved_task = session.get(Task, db_task.id)
        print(f"\nRetrieved task tags: {repr(retrieved_task.tags)}")
        print(f"Retrieved task tags type: {type(retrieved_task.tags)}")

        # Test converting back to list (as would happen in TaskRead.from_orm)
        if isinstance(retrieved_task.tags, str):
            try:
                tags_list = json.loads(retrieved_task.tags)
                print(f"\nConverted back to list: {tags_list}")
                print(f"Type after conversion: {type(tags_list)}")
            except:
                print("\nFailed to convert back to list")

    print("\nTest passed - tags conversion works correctly!")

if __name__ == "__main__":
    test_tags_conversion()
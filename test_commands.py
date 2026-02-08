#!/usr/bin/env python3
"""
Test script to verify chatbot commands work correctly
"""

import re
from datetime import datetime

def test_intent_analysis():
    """Test the intent analysis function"""
    message = "Update task 1 to have description 'project deployment and advance features'"
    message_lower = message.lower().strip()

    print(f"Testing message: '{message}'")
    print(f"Lowercase: '{message_lower}'")

    # Test intent analysis
    intent_patterns = {
        "add_task": any(word in message_lower for word in ["add", "create", "new", "make"]) and any(word in message_lower for word in ["task", "todo", "item"]),
        "list_tasks": any(word in message_lower for word in ["list", "show", "display", "view", "get"]) and any(word in message_lower for word in ["task", "todo", "item", "all"]),
        "update_task": any(word in message_lower for word in ["update", "change", "modify", "edit"]) and any(word in message_lower for word in ["task", "todo", "item"]),
        "complete_task": any(word in message_lower for word in ["complete", "done", "finish", "mark"]) and any(word in message_lower for word in ["task", "todo", "item"]),
        "delete_task": any(word in message_lower for word in ["delete", "remove", "erase", "cancel"]) and any(word in message_lower for word in ["task", "todo", "item"]),
    }

    print("Intent analysis:")
    for intent, matched in intent_patterns.items():
        print(f"  {intent}: {matched}")

    # Check if 'date' substring exists anywhere
    has_date_substring = 'date' in message_lower
    print(f"\nContains 'date' substring: {has_date_substring}")

    # Check for specific phrases that should trigger date response
    specific_date_phrases = ['what date', 'today\'s date']
    triggers_date_response = any(phrase in message_lower for phrase in specific_date_phrases)
    print(f"Triggers date response (specific phrases): {triggers_date_response}")

def test_update_regex():
    """Test the update task regex patterns"""
    message = "Update task 1 to have description 'project deployment and advance features'"

    # Test ID matching
    id_match = re.search(r"(?:update|change|modify|edit)\s+task\s+(\d+)", message.lower())
    print(f"\nTesting ID extraction from: '{message}'")
    if id_match:
        task_id = int(id_match.group(1))
        print(f"  Found task ID: {task_id}")
    else:
        print("  No task ID found!")

    # Test title matching
    title_match = re.search(r"(?:title|name|to)\s+(?:is\s+|to\s+have\s+)?['\"](.+?)['\"]", message)
    print(f"\nTesting title extraction:")
    if title_match:
        title = title_match.group(1)
        print(f"  Found title: '{title}'")
    else:
        print("  No title found!")

    # Test description matching
    desc_match = re.search(r"(?:to\s+have\s+)?(?:description|desc|details)\s+(?:is\s+|to\s+have\s+)?['\"](.+?)['\"]", message)
    print(f"\nTesting description extraction:")
    if desc_match:
        desc = desc_match.group(1)
        print(f"  Found description: '{desc}'")
    else:
        print("  No description found!")

def test_time_date_detection():
    """Test time/date detection in various messages"""
    test_messages = [
        "Update task 1 to have description 'project deployment and advance features'",
        "What time is it?",
        "What's the date today?",
        "Show me my tasks",
        "Add a task to buy groceries",
        "Complete task 3",
        "Update task 2 with new deadline",
        "Tell me the time",
        "What's today's date?",
        "Deployment task update"
    ]

    print("\nTesting time/date detection in various messages:")
    for msg in test_messages:
        msg_lower = msg.lower()

        # Old way (problematic)
        old_date_check = 'date' in msg_lower
        old_time_check = 'time' in msg_lower

        # New way (specific phrases)
        new_date_check = any(phrase in msg_lower for phrase in ['what date', 'what\'s the date', 'today\'s date'])
        new_time_check = any(phrase in msg_lower for phrase in ['what time', 'what\'s the time'])

        print(f"  '{msg}'")
        print(f"    Old date check: {old_date_check}, New date check: {new_date_check}")
        print(f"    Old time check: {old_time_check}, New time check: {new_time_check}")
        print()

if __name__ == "__main__":
    print("Testing chatbot command processing...")
    print("=" * 50)

    test_intent_analysis()
    test_update_regex()
    test_time_date_detection()

    print("Tests completed!")
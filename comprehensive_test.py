#!/usr/bin/env python3
"""
Comprehensive test of all chatbot commands
"""

import re
from datetime import datetime

def analyze_command(message):
    """Analyze a command and return what the system should do with it"""
    print(f"\nAnalyzing: '{message}'")

    message_lower = message.lower().strip()

    # Intent analysis
    if any(word in message_lower for word in ["add", "create", "new", "make"]) and any(word in message_lower for word in ["task", "todo", "item"]):
        intent = "add_task"
    elif any(word in message_lower for word in ["list", "show", "display", "view", "get"]) and any(word in message_lower for word in ["task", "todo", "item", "all"]):
        intent = "list_tasks"
    elif any(word in message_lower for word in ["update", "change", "modify", "edit"]) and any(word in message_lower for word in ["task", "todo", "item"]):
        intent = "update_task"
    elif any(word in message_lower for word in ["complete", "done", "finish", "mark"]) and any(word in message_lower for word in ["task", "todo", "item"]):
        intent = "complete_task"
    elif any(word in message_lower for word in ["delete", "remove", "erase", "cancel"]) and any(word in message_lower for word in ["task", "todo", "item"]):
        intent = "delete_task"
    else:
        intent = "general"

    print(f"  Intent: {intent}")

    # Check for time/date triggers (new improved logic)
    triggers_time_old = 'time' in message_lower
    triggers_date_old = 'date' in message_lower
    triggers_time_new = any(phrase in message_lower for phrase in ['what time is it', 'what\'s the time', 'tell me the time'])
    triggers_date_new = any(phrase in message_lower for phrase in ['what date is it', 'what\'s the date', 'today\'s date'])

    print(f"  Old time trigger: {triggers_time_old}, New time trigger: {triggers_time_new}")
    print(f"  Old date trigger: {triggers_date_old}, New date trigger: {triggers_date_new}")

    # For update tasks, extract details
    if intent == "update_task":
        id_match = re.search(r"(?:update|change|modify|edit)\s+task\s+(\d+)", message_lower)
        if id_match:
            print(f"  Task ID to update: {id_match.group(1)}")

        # Check for title and description
        title_match = re.search(r"(?:title|name|to)\s+(?:is\s+|to\s+have\s+)?['\"](.+?)['\"]", message)
        desc_match = re.search(r"(?:to\s+have\s+)?(?:description|desc|details)\s+(?:is\s+|to\s+have\s+)?['\"](.+?)['\"]", message)

        if title_match:
            print(f"  New title: '{title_match.group(1)}'")
        if desc_match:
            print(f"  New description: '{desc_match.group(1)}'")

    # For add tasks, extract details
    if intent == "add_task":
        # Simple extraction for testing
        if "to" in message:
            title = message.split("to")[1].strip().split("'")[0] if "'" in message else message.split("to")[1].strip()
            print(f"  Task to create: '{title}'")

    # For complete/delete tasks, extract task ID
    if intent in ["complete_task", "delete_task"]:
        id_match = re.search(r'task\s+(\d+)', message_lower)
        if id_match:
            print(f"  Task ID: {id_match.group(1)}")

    return intent

def run_comprehensive_tests():
    """Test all major command types"""

    test_commands = [
        # Update commands
        "Update task 1 to have description 'project deployment and advance features'",
        "Update task 2 to have title 'Buy groceries'",
        "Change task 3 description to 'Updated description here'",
        "Modify task 4 to have title 'New Title' and description 'New Description'",

        # Add commands
        "Add a task to buy groceries",
        "Create task: finish project documentation",
        "Make a new task to call mom",
        "Add task 'walk the dog' with description 'every evening'",

        # List commands
        "Show me my tasks",
        "List all tasks",
        "Display my pending tasks",
        "Show completed tasks",

        # Complete commands
        "Complete task 1",
        "Mark task 2 as done",
        "Finish task 3",

        # Delete commands
        "Delete task 1",
        "Remove task 2",
        "Cancel task 3",

        # Time/date commands (should NOT trigger anymore)
        "What time is it?",
        "What's the date today?",
        "Tell me the time",
        "What's today's date?",

        # Problematic commands that contain 'date' substring
        "Update task 1 with deployment schedule",
        "Task about database optimization",
        "Update the deadline for task 2",
        "Schedule the date for the event"
    ]

    print("Running comprehensive command tests...")
    print("=" * 60)

    for command in test_commands:
        analyze_command(command)

    print("\n" + "=" * 60)
    print("All tests completed!")

if __name__ == "__main__":
    run_comprehensive_tests()
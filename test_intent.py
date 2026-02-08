#!/usr/bin/env python3
"""
Test the intent analysis logic specifically
"""

def analyze_intent(message: str) -> str:
    """
    Analyze the user message to determine the intent.
    Order matters - check more specific intents first
    """
    message_lower = message.lower().strip()

    # Define patterns for different intents - order matters
    if any(word in message_lower for word in ["update", "change", "modify", "edit"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "update_task"

    if any(word in message_lower for word in ["add", "create", "new", "make"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "add_task"

    if any(word in message_lower for word in ["list", "show", "display", "view", "get"]):
        if any(word in message_lower for word in ["task", "todo", "item", "all"]):
            return "list_tasks"

    if any(word in message_lower for word in ["complete", "done", "finish", "mark"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "complete_task"

    if any(word in message_lower for word in ["delete", "remove", "erase", "cancel"]):
        if any(word in message_lower for word in ["task", "todo", "item"]):
            return "delete_task"

    # Default to general query
    return "general"

def test_specific_cases():
    test_cases = [
        "Modify task 4 to have title 'New Title' and description 'New Description'",
        "Add a task to buy groceries",
        "Update task 1 to have description 'project deployment and advance features'",
        "Create task: finish project documentation",
        "Change task 3 description to 'Updated description here'"
    ]

    for case in test_cases:
        intent = analyze_intent(case)
        print(f"'{case}' -> {intent}")

if __name__ == "__main__":
    test_specific_cases()
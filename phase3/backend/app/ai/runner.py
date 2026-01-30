from typing import Dict, Any, List
from sqlmodel import Session
from openai import OpenAI
import json
import os
from .agent import setup_mcp_server


class OpenAIChatRunner:
    def __init__(self, db: Session):
        self.db = db

        # Check if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.client = OpenAI(api_key=api_key)

        # Setup MCP server to get tools
        self.mcp_server = setup_mcp_server(db)
        self.tools = self.mcp_server.get_openai_tools()

    def run_assistant(self, user_message: str, user_id: int) -> Dict[str, Any]:
        """
        Run the OpenAI assistant with MCP tools for task management
        """
        try:
            # Prepare the initial message with context
            messages = [
                {
                    "role": "system",
                    "content": f"You are an AI assistant for managing tasks. The current user ID is {user_id}. "
                               f"Always use the appropriate tools to manage tasks. "
                               f"Be helpful but only perform actions through tools."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]

            # Make the API call with function calling
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # You can change this to gpt-4 if preferred
                messages=messages,
                tools=self.tools,
                tool_choice="auto"  # Let the model decide when to use tools
            )

            # Get the response message
            response_message = response.choices[0].message

            # Check if the model wanted to call any tools
            tool_calls = response_message.tool_calls

            if tool_calls:
                # Extend conversation with assistant's request to call tools
                messages.append(response_message)

                # Execute all tool calls and collect results
                tool_call_results = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Ensure user_id is passed as a string as expected by our tools
                    if "user_id" not in function_args:
                        function_args["user_id"] = str(user_id)
                    else:
                        # Ensure user_id is always set to the current user's ID
                        function_args["user_id"] = str(user_id)

                    # Call the appropriate tool
                    try:
                        tool_result = self.mcp_server.call_tool(function_name, function_args)

                        # Add result to messages
                        tool_call_results.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(tool_result)
                        })
                    except Exception as e:
                        error_result = {
                            "error": str(e),
                            "function_name": function_name
                        }
                        tool_call_results.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": json.dumps(error_result)
                        })

                # Add all tool results to messages
                messages.extend(tool_call_results)

                # Get final response from assistant after tool results
                final_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )

                final_message = final_response.choices[0].message

                return {
                    "response": final_message.content,
                    "tool_calls": [{
                        "name": tc.function.name,
                        "arguments": json.loads(tc.function.arguments),
                        "result": next(tr for tr in tool_call_results if tr["tool_call_id"] == tc.id)["content"]
                    } for tc in tool_calls]
                }
            else:
                # No tools were called, return the direct response
                return {
                    "response": response_message.content,
                    "tool_calls": []
                }

        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "tool_calls": []
            }


def run_chat_completion(user_message: str, user_id: int, db: Session) -> Dict[str, Any]:
    """
    Main function to run chat completion with OpenAI and MCP tools
    """
    try:
        runner = OpenAIChatRunner(db)
        return runner.run_assistant(user_message, user_id)
    except ValueError as e:
        # Fallback to the original agent if OpenAI API key is not available
        from .agent import process_user_message

        # The process_user_message function now returns a dict with 'response' and 'tool_calls'
        # so we can return it directly
        result = process_user_message(user_message, user_id, db)

        # Ensure it has the right format for the API
        if isinstance(result, str):
            # If it returns a string (old format), convert to new format
            return {
                "response": result,
                "tool_calls": []
            }
        else:
            # If it returns a dict (new format), return as is
            return result
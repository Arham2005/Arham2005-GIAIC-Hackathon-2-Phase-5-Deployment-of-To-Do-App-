from typing import Dict, Any, List
from sqlmodel import Session
import json


class MCPServer:
    def __init__(self, db: Session):
        self.db = db
        self.tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, func: callable, description: str = "", parameters: Dict[str, Any] = None):
        """
        Register a tool with the MCP server following OpenAI function calling format
        """
        if parameters is None:
            parameters = {
                "type": "object",
                "properties": {},
                "required": []
            }

        self.tools[name] = {
            "function": func,
            "description": description,
            "parameters": parameters
        }

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a registered tool with the provided arguments
        """
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered")

        tool_info = self.tools[name]
        tool_func = tool_info["function"]

        # Check if the function expects a db parameter
        import inspect
        sig = inspect.signature(tool_func)
        params = dict(arguments)

        if 'db' in sig.parameters:
            params['db'] = self.db

        return tool_func(**params)

    def get_tool_names(self) -> list:
        """
        Get a list of registered tool names
        """
        return list(self.tools.keys())

    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """
        Get tools in OpenAI-compatible format for function calling
        """
        openai_tools = []
        for name, tool_info in self.tools.items():
            openai_tool = {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool_info["description"],
                    "parameters": tool_info["parameters"]
                }
            }
            openai_tools.append(openai_tool)
        return openai_tools

    def get_tool_by_name(self, name: str) -> Dict[str, Any]:
        """
        Get a specific tool definition by name
        """
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered")
        return self.tools[name]
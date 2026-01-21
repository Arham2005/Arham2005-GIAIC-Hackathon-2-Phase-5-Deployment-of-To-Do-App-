from typing import Dict, Callable, Any
from sqlmodel import Session


class MCPServer:
    def __init__(self, db: Session):
        self.db = db
        self.tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        """
        Register a tool with the MCP server
        """
        self.tools[name] = func

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a registered tool with the provided arguments
        """
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered")

        # Add the database session to the arguments
        tool_func = self.tools[name]

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

    def get_tool_schema(self, name: str) -> Dict[str, Any]:
        """
        Get the schema for a specific tool (for AI model consumption)
        """
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered")

        # This would typically return a JSON schema for the tool
        # For now, we'll return a basic schema based on function signature
        import inspect
        sig = inspect.signature(self.tools[name])

        properties = {}
        required = []
        for param_name, param in sig.parameters.items():
            # Skip 'db' parameter as it's injected by the server
            if param_name == 'db':
                continue

            properties[param_name] = {"type": "string"}  # Simplified
            required.append(param_name)

        return {
            "name": name,
            "description": getattr(self.tools[name], '__doc__', ''),
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required
            }
        }
import asyncio
from typing import Any, Dict, List, Optional
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClient:
    """A client to interact with an MCP server."""
    def __init__(self, command: str, args: List[str]):
        self.server_params = StdioServerParameters(
            command=command,
            args=args,
            env=None
        )
        self.session: Optional[ClientSession] = None
        self._exit_stack = None

    async def connect(self):
        """Connects to the MCP server."""
        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        read_stream, write_stream = await self._exit_stack.enter_async_context(stdio_client(self.server_params))
        self.session = await self._exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
        await self.session.initialize()

    async def disconnect(self):
        """Disconnects from the MCP server."""
        if self._exit_stack:
            await self._exit_stack.aclose()
            self.session = None

    async def list_tools(self) -> List[Dict[str, Any]]:
        """Lists available tools on the server and returns them as a list of dicts."""
        if not self.session:
            raise RuntimeError("Client is not connected.")
        result = await self.session.list_tools()
        # Convert Tool objects to dictionaries for easier use in UI/logic
        return [tool.model_dump() if hasattr(tool, 'model_dump') else vars(tool) for tool in result.tools]

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Calls a specific tool on the server."""
        if not self.session:
            raise RuntimeError("Client is not connected.")
        result = await self.session.call_tool(name, arguments)
        # Convert content to dicts if possible
        return [content.model_dump() if hasattr(content, 'model_dump') else vars(content) for content in result.content]
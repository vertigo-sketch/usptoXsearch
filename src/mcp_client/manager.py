import asyncio
from typing import Any, Dict, List, Optional, Callable
from src.mcp_client.client import MCPClient

class MCPManager:
    """Manages the lifecycle and interaction with the MCP client."""
    def __init__(self, command: str, args: List[str]):
        self.client = MCPClient(command, args)
        self._loop = asyncio.new_event_loop()
        import threading
        self._thread = threading.Thread(target=self._run_event_loop, daemon=True)
        self._thread.start()

    def _run_event_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def run_async(self, coro: Any):
        """Schedules a coroutine to be run in the background loop."""
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    async def connect(self):
        await self.client.connect()

    async def disconnect(self):
        await self.client.disconnect()

    async def list_tools(self) -> List[Dict[str, Any]]:
        return await self.client.list_tools()

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
        return await self.client.call_tool(name, arguments)
import asyncio
import sys
from pathlib import Path

from fastmcp.client.transports import PythonStdioTransport
from langchain.mcp import MCPAdapter
from rich.console import Console

console = Console()


async def Main():
    transport = PythonStdioTransport(
        script_path=str(Path(__file__).with_name("mcpServer.py")),
        python_cmd=sys.executable,
    )

    async with MCPAdapter(transport) as client:
        tools = await client.list_tools()
        console.log("yeh hai mere tools", tools)


if __name__ == "__main__":
    asyncio.run(Main())

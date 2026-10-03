# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "langchain-mcp-adapters==0.3.1",
#     "mcp>=1.24.0,<2",
#     "rich>=15.0.0",
# ]
# ///
# Run with: uv run --script src/ragagent/streamHttp/multipleServer.py
# The client uses MCP 1 in isolation; the FastMCP servers use MCP 2.

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from rich.console import Console

console = Console()


async def Main():
    client = MultiServerMCPClient(
        {
            "mcpServer": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp",
            },
            "httpMcpTool": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8001/mcp",
            },
        }
    )
    tools = await client.get_tools()
    console.log("yeh hai mere tools", tools)
    console.log("Total tools:", len(tools))


if __name__ == "__main__":
    asyncio.run(Main())

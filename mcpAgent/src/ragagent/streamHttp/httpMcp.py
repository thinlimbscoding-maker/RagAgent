import asyncio

from fastmcp.client.transports import StreamableHttpTransport
from langchain.mcp import MCPAdapter
from rich.console import Console

console = Console()


async def Main():
    transport = StreamableHttpTransport(url="http://localhost:8000/mcp")

    async with MCPAdapter(transport) as client:
        tools = await client.list_tools()
        console.log("yeh hai mere tools", tools)


if __name__ == "__main__":
    asyncio.run(Main())

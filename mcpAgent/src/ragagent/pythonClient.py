import os
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters, client
import asyncio
from rich.console import Console

console = Console()

# path for client
mcp_server_script = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "mcpServer.py"
)

print(mcp_server_script)


# server parameter
server_params = StdioServerParameters(
    env={}, command="python", args=[str(mcp_server_script)]
)


# cleint session
async def Main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tool = await session.list_tools()
            # console.print("[bold cyan]Available MCP tools[/bold cyan]")
            console.print_json(tool.model_dump_json(exclude_none=True))
            console.log({"name": ":ssas"})
            result = await session.call_tool(
                "fetchGender", arguments={"path": "/anypath"}
            )
            console.log("result", result)


if __name__ == "__main__":
    asyncio.run(Main())

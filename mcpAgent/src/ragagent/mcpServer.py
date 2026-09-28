from fastmcp import FastMCP

mcp = FastMCP()


@mcp.tool()
def fetchData():
    return "we got data"


@mcp.tool()
def fetchInfo():
    return "we got info"


@mcp.tool()
def fetchGender(path: str):
    return "we got fetaGender"


if __name__ == "__main__":
    mcp.run(transport="stdio")

import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=("stdio", "http"), default="stdio")
    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="http", host="127.0.0.1", port=8000)
    else:
        mcp.run(transport="stdio")

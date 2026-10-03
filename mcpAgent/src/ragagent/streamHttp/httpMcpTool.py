import argparse
import requests
from fastmcp import FastMCP

mcp = FastMCP()


@mcp.tool()
def fetchData2():
    return "we got data2"


@mcp.tool()
def fetchInfo2():
    return "we got info2"


@mcp.tool()
def fetchGender2(path: str):
    return "we got fetaGender2"


@mcp.tool()
def getAPiData2():
    url = "https://jsonplaceholder.typicode.com/todos/1"

    try:
        # Send the GET request
        response = requests.get(url, timeout=5)

        # Check if the request was successful (Status Code 200)
        if response.status_code == 200:
            # Parse the response data into a Python dictionary
            data = response.json()

            return data
        else:
            return {
                "error": f"Failed to retrieve data. Status code: {response.status_code}"
            }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", choices=("stdio", "http"), default="stdio")
    args = parser.parse_args()

    if args.transport == "http":
        mcp.run(transport="http", host="127.0.0.1", port=8001)
    else:
        mcp.run(transport="stdio")

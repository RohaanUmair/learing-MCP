from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name='hello-mcp', stateless_http=True)


@mcp.tool(name='Online_researcher', description="This tool searches online and return result")
def search_online(query: str) -> str:
    return f'Searching for {query}...'

@mcp.tool()
def get_weather(city: str) -> str:
    return f'Weather in {city} is Sunny.'

@mcp.tool(name="read_file", description="Read contents of a local text file. Input must be the full file path or a filename in the current directory.")
def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"




mcp_app = mcp.streamable_http_app()
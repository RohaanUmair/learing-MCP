from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name='hello-mcp', stateless_http=True)


@mcp.tool(name='Online Researher', description="This tool searches online and return result")
def search_online(query: str) -> str:
    return f'Searching for {query}...'

@mcp.tool()
def get_weather(city: str) -> str:
    return f'Weather in {city} is Sunny.'


mcp_app = mcp.streamable_http_app()
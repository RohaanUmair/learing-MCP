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

@mcp.tool(name="edit_file", description="Edit a local text file by appending or replacing content")
def edit_file(path: str, content: str, mode: str = "overwrite") -> str:
    """
    Edit a file with given content.
    mode = "append" -> adds content at the end
    mode = "overwrite" -> replaces entire file content
    """
    try:
        if mode == "overwrite":
            with open(path, "w") as f:
                f.write(content)
            return f"File '{path}' overwritten with new content."
        else:  # append
            with open(path, "a") as f:
                f.write("\n" + content)
            return f"Appended new content to '{path}'."
    except Exception as e:
        return f"Error editing file: {e}"



mcp_app = mcp.streamable_http_app()
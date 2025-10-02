from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name='hello-mcp', stateless_http=True)


@mcp.tool(
    name="read_file",
    description="Read contents of a local text file. Input the file path or filename in the current directory. Example: 'dummyfile.txt'. Whatever user gives filename, check for it in current directory only."
)
def read_file(path: str) -> str:
    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"


@mcp.tool(name="edit_file", description="Edit a local text file by appending or replacing content. Input the file path or filename in the current directory. Example: 'dummyfile.txt'. Whatever user gives filename, check for it in current directory only.")
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


@mcp.tool(
    name="knowledge_lookup_about_rohaan", 
    description="Provides Rohaan's personal info: name, age, profession, skills, education, projects, hobbies. Use this tool to answer any questions about Rohaan."
)
def knowledge_lookup(query: str) -> str:
    rohaan_data = {
        "name": "Muhammad Rohaan Umair",
        "age": "19",
        "profession": "Full-stack Web Developer and AI Developer",
        "skills": "MERN stack, Next.js, Express.js, MongoDB, React.js, Agentic AI, MCP",
        "education": "Completed O-levels, currently Intermediate, studying at SMIT (Saylani Mass IT Training)",
        "projects": "Recipe website, Movie website, Todo app, RAG chatbot with MCP integration",
        "hobbies": "Problem-solving, AI experiments, building web apps"
    }

    query_lower = query.lower()
    for key, value in rohaan_data.items():
        if key in query_lower:
            return value

    if any(word in query_lower for word in ["rohaan", "about", "info", "details"]):
        summary = (
            f"{rohaan_data['name']}, age {rohaan_data['age']}, is a {rohaan_data['profession']}. "
            f"Skills: {rohaan_data['skills']}. Education: {rohaan_data['education']}. "
            f"Projects: {rohaan_data['projects']}. Hobbies: {rohaan_data['hobbies']}."
        )
        return summary

    return "No data found about Rohaan."


@mcp.tool(
    name="get_product_price",
    description="Retrieve the price of a product by its name."
)
def get_product_price(product_name: str) -> str:
    import requests

    try:
        url = f"https://dummyjson.com/products/search?q={product_name}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "products" not in data or not data["products"]:
            return f"No product found for '{product_name}'."

        product = data["products"][0]
        title = product.get("title", "Unknown Product")
        price = product.get("price", "Unknown Price")
        availability = product.get("availabilityStatus", "Unknown")

        return f"{title} costs ${price}. Availability: {availability}."

    except Exception as e:
        return f"Error fetching product price: {e}"




app = mcp.streamable_http_app()
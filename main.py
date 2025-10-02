import asyncio
import os
from dotenv import load_dotenv, find_dotenv

from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams


_: bool = load_dotenv(find_dotenv())

MCP_SERVER_URL = "http://localhost:8000/mcp"

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

async def main():
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
    print(f"MCPServerStreamableHttpParams configured for URL: {mcp_params.get('url')}")

    async with MCPServerStreamableHttp(params=mcp_params, name="MySharedMCPServerClient") as mcp_server_client:
        try:
            assistant = Agent(
                name="MyMCPConnectedAssistant",
                mcp_servers=[mcp_server_client],
                model=OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client),
            )
            
            tools = await mcp_server_client.list_tools()
            print(f"Tools: {tools}")

            print("\n\nRunning a simple agent interaction...\n\n")
            
            user_input = input('User: ')
            result = await Runner.run(assistant, user_input)
            print(f"\n\n[AGENT RESPONSE]: {result.final_output}")

        except Exception as e:
            print(f"An error occurred during agent setup or tool listing: {e}")

    print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' context exited.")
    print(f"--- Agent Connection Test End ---")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An unhandled error occurred in the agent script: {e}")


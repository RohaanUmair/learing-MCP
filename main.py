import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from agents.run import RunConfig
from agents import Agent, AsyncOpenAI, OpenAIChatCompletionsModel, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams


_: bool = load_dotenv(find_dotenv())
os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

MCP_SERVER_URL = "http://localhost:8000/mcp"

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

async def main():
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)

    async with MCPServerStreamableHttp(params=mcp_params, name="MySharedMCPServerClient") as mcp_server_client:
        try:
            assistant = Agent(
                name="MyMCPConnectedAssistant",
                mcp_servers=[mcp_server_client],
                model=model,
            )
            
            tools = await mcp_server_client.list_tools()
            print(f"Tools: {tools}")

            print("\n\nRunning a simple agent interaction...\n\n")
            
            
            while True:
                user_input = input('[USER]: ')
                result = await Runner.run(assistant, user_input, run_config=config)
                print(f"[AGENT RESPONSE]: {result.final_output}")

        except Exception as e:
            print(f"An error occurred during agent setup or tool listing: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An unhandled error occurred in the agent script: {e}")


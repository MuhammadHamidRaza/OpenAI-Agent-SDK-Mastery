import asyncio
from agents import Agent, Runner, SQLiteSession, function_tool, run_demo_loop, ModelSettings, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os
from openai import AsyncOpenAI

load_dotenv()
# Change to GEMINI_API_KEY check
if "GEMINI_API_KEY" not in os.environ:
    print("Please set GEMINI_API_KEY in your environment.")
    raise SystemExit(1)

# Gemini client setup
client = AsyncOpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"), # Use GEMINI_API_KEY from env
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model
gemini_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", # Or another appropriate Gemini model
    openai_client=client
)

# Tool
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

# Agent
agent = Agent(
    name="SmartChatBuddy",
    instructions="You’re a helpful assistant who uses tools for math and keeps answers short.",
    tools=[add_numbers],
    model=gemini_model # Pass the Gemini model
)

async def main():
 
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())
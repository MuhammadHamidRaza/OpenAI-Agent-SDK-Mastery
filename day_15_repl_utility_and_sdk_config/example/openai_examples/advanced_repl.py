import asyncio
from agents import Agent, Runner, SQLiteSession, function_tool, run_demo_loop, ModelSettings
from dotenv import load_dotenv
import os

load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("Please set OPENAI_API_KEY in your environment.")
    raise SystemExit(1)

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
)

async def main():
 
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())

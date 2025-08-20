import asyncio
from agents import WebSearchTool

from agents import Agent, Runner

agent = Agent(
    name="SearchBuddy",
    instructions="Answer user questions using web search when needed.",
    tools=[WebSearchTool()],
)

async def main():
    result = await Runner.run(agent, "What's the latest news about artificial intelligence?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
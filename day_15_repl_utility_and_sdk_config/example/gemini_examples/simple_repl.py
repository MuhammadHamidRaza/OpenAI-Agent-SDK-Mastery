import asyncio
from agents import Agent, run_demo_loop, OpenAIChatCompletionsModel, Runner
from openai import AsyncOpenAI

# Gemini client setup
client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", # Or another appropriate Gemini model
    openai_client=client
)

async def main() -> None:
    agent = Agent(name="Assistant", instructions="You are a helpful assistant.", model=model)
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())
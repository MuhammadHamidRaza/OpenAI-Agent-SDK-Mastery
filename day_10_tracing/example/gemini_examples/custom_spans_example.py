import asyncio
from agents import Agent, Runner, trace, span, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
import os

# Gemini client setup
client = AsyncOpenAI(
    api_key="YOUR_GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

async def main():
    agent = Agent(name="MyAgent", instructions="You are a helpful assistant.", model=model)

    with trace("MyWorkflow"):
        with span("MyCustomSpan"):
            # Your custom logic here
            print("This is a custom span.")

        await Runner.run(agent, "Hello, world!")

if __name__ == "__main__":
    asyncio.run(main())
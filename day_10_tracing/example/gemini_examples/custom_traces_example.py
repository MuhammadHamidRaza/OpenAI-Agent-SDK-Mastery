import asyncio
from agents import Agent, Runner, trace, OpenAIChatCompletionsModel
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
    agent = Agent(name="JokeAgent", instructions="Tell me a joke.", model=model)

    with trace("JokeWorkflow"):
        # First run
        result1 = await Runner.run(agent, "Tell me a joke about cats.")
        print(f"Joke: {result1.final_output}")

        # Second run, grouped in the same trace
        result2 = await Runner.run(agent, "Now tell me one about dogs.")
        print(f"Joke: {result2.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
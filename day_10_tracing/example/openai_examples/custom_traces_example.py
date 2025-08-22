import asyncio
from agents import Agent, Runner, trace
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

async def main():
    agent = Agent(name="JokeAgent", instructions="Tell me a joke.")

    with trace("JokeWorkflow"):
        # First run
        result1 = await Runner.run(agent, "Tell me a joke about cats.")
        print(f"Joke: {result1.final_output}")

        # Second run, grouped in the same trace
        result2 = await Runner.run(agent, "Now tell me one about dogs.")
        print(f"Joke: {result2.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
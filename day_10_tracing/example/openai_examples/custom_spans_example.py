import asyncio
from agents import Agent, Runner, trace, span
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

async def main():
    agent = Agent(name="MyAgent", instructions="You are a helpful assistant.")

    with trace("MyWorkflow"):
        with span("MyCustomSpan"):
            # Your custom logic here
            print("This is a custom span.")

        await Runner.run(agent, "Hello, world!")

if __name__ == "__main__":
    asyncio.run(main())
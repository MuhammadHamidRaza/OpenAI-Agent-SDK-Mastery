import asyncio
from agents import Agent, Runner, Session, function_tool
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY in the .env file.")
    exit()

# Define a math tool
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

# Define the General Agent
general_agent = Agent(
    name="HelperBuddy",
    instructions="You’re a friendly assistant who answers general questions. For math questions, hand off to MathBuddy."
)

# Define the Math Agent with a tool
math_agent = Agent(
    name="MathBuddy",
    instructions="You’re a math expert who uses tools to answer math questions.",
    tools=[add_numbers]
)

# Create a Session
session = Session()

async def main():
    runner = Runner()
    # Ask a general question with tracing
    print("General Question:")
    result1 = await runner.run(
        general_agent,
        "What’s a bird?",
        session=session
    )
    print("Answer:", result1.final_output)
    # print("Messages:", result1.messages) # Uncomment for full messages
    # print("Status:", result1.status)     # Uncomment for status

    # Ask a math question (handoff to MathBuddy with tool)
    print("\nMath Question:")
    result2 = await runner.run(
        general_agent,
        "What’s 7 plus 3?",
        session=session
    )
    print("Answer:", result2.final_output)

    # Ask a follow-up question
    print("\nFollow-Up Question:")
    result3 = await runner.run(
        general_agent,
        "Can they fly?",
        session=session
    )
    print("Answer:", result3.final_output)

if __name__ == "__main__":
    asyncio.run(main())

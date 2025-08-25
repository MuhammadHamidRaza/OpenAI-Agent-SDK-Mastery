from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY in the .env file.")
    exit()

# Define the General Agent
general_agent = Agent(
    name="HelperBuddy",
    instructions="You’re a friendly assistant who answers general questions. For math questions, hand off to MathBuddy."
)

# Define the Math Agent
math_agent = Agent(
    name="MathBuddy",
    instructions="You’re a math expert who answers math questions in short replies."
)

# Create a Runner
runner = Runner()

# Ask a general question
result1 = runner.run_sync(
    general_agent,
    "What’s a fish?"
)
print("General Answer:", result1.final_output)

# Ask a math question (handoff to MathBuddy)
result2 = runner.run_sync(
    general_agent,
    "What is 6 plus 9?"
)
print("Math Answer:", result2.final_output)
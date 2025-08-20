from agents import Agent, Runner
from agents.tools import function_tool
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define the add_numbers tool (from Day 5)
@function_tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the sum.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of the two numbers.
    """
    return a + b

# Define the Agent and pass the tool to it
calculator_agent = Agent(
    name="CalculatorAgent",
    instructions="You are a helpful assistant that can perform arithmetic operations. Use the provided tools to calculate sums.",
    tools=[add_numbers] # <--- Here we pass the tool to the agent
)

# Run the agent with a prompt that requires the tool
print("Running CalculatorAgent...")
result = Runner.run_sync(calculator_agent, "What is 123.45 + 67.89?")

# Print the final output from the agent
print("Agent's response:", result.final_output)

# Another example
print("\nRunning CalculatorAgent with another sum...")
result2 = Runner.run_sync(calculator_agent, "Can you tell me the sum of 500 and 750?")
print("Agent's response:", result2.final_output)

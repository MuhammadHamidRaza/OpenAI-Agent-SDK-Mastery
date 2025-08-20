from agents import Agent, Runner
from agents.tools import function_tool
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define the greet_user tool (from Day 5)
@function_tool
def greet_user(name: str) -> str:
    """Generates a personalized greeting for a user.

    Args:
        name: The name of the user to greet.

    Returns:
        A personalized greeting string.
    """
    return f"Hello, {name}! Nice to meet you."

# Define the Agent and pass the tool to it
greeter_agent = Agent(
    name="GreeterAgent",
    instructions="You are a friendly assistant that can greet people by name using the provided tool.",
    tools=[greet_user] # <--- Here we pass the tool to the agent
)

# Run the agent with a prompt that requires the tool
print("\nRunning GreeterAgent...")
result = Runner.run_sync(greeter_agent, "Please greet John Doe.")

# Print the final output from the agent
print("Agent's response:", result.final_output)

# Another example
print("\nRunning GreeterAgent with another name...")
result2 = Runner.run_sync(greeter_agent, "Say hello to Alice.")
print("Agent's response:", result2.final_output)

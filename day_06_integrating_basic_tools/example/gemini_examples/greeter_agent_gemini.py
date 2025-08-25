from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.tools import function_tool
from openai import AsyncOpenAI
import os

client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

@function_tool
def greet_user(name: str) -> str:
    """Generates a personalized greeting for a user.

    Args:
        name: The name of the user to greet.

    Returns:
        A personalized greeting string.
    """
    return f"Hello, {name}! Nice to meet you."

greeter_agent = Agent(
    name="GreeterAgent",
    instructions="You are a friendly assistant that can greet people by name using the provided tool.",
    tools=[greet_user],
    model=model
)

print("\nRunning GreeterAgent...")
result = Runner.run_sync(greeter_agent, "Please greet John Doe.")
print("Agent's response:", result.final_output)

print("\nRunning GreeterAgent with another name...")
result2 = Runner.run_sync(greeter_agent, "Say hello to Alice.")
print("Agent's response:", result2.final_output)
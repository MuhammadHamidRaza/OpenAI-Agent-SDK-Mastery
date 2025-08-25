from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

@function_tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two integers and return the product."""
    return a * b

math_agent = Agent(
    name="MathBuddy",
    handoff_description="Specialist for arithmetic and other math questions.",
    instructions="You are a math expert. Prefer using tools for calculations.",
    tools=[multiply_numbers],
    model=model
)

# Example usage (assuming general_agent from simple_multi_agent.py exists)
# r3 = Runner.run_sync(general_agent, "What is 5 times 6?")
# print("Math with tool:", r3.final_output)
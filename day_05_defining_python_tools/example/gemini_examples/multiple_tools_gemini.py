from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# ✅ Gemini client setup
client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

@function_tool
def multiply(x: int, y: int) -> int:
    return x * y

agent = Agent(name="Calc", instructions="Use tools for math.", tools=[add_numbers, multiply], model=model)

# Example usage (not in original, but for completeness)
result = Runner.run_sync(agent, "What is 7 times 5?")
print(result.final_output)

result = Runner.run_sync(agent, "What is 10 plus 20?")
print(result.final_output)

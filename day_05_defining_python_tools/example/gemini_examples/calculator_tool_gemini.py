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

# Create the agent and register the tool
agent = Agent(
    name="MathBuddy",
    instructions="You are a helpful assistant who uses tools to answer math questions.",
    tools=[add_numbers],
    model=model
)

# Run synchronously (one-off script)
result = Runner.run_sync(agent, "What is 7 plus 5?")
print(result.final_output)

from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.tools import function_tool
from openai import AsyncOpenAI
import os
from datetime import datetime
import pytz

client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

@function_tool
def get_current_time(timezone: str = "UTC") -> str:
    """Returns the current time in a specified timezone.

    Args:
        timezone: The timezone to get the time for (e.g., "America/New_York", "UTC"). Defaults to "UTC".

    Returns:
        A string representing the current time.
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        return now.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    except pytz.UnknownTimeZoneError:
        return f"Error: Unknown timezone '{timezone}'."

agent = Agent(
    name="TimeAgent",
    instructions="You are a helpful assistant that can tell the current time.",
    tools=[get_current_time],
    model=model
)

print("Running TimeAgent...")
result = Runner.run_sync(agent, "What time is it in New York?")

print("\n--- RunResult Inspection ---")
print(f"Final Output: {result.final_output}")
print(f"Original Input: {result.input}")
print(f"Last Agent: {result.last_agent.name}")

print("\nNew Items (Chronological Events):")
for item in result.new_items:
    print(f"  - Type: {type(item).__name__}")
    if hasattr(item, 'text'):
        print(f"    Text: {item.text[:50]}...")
    if hasattr(item, 'tool_name'):
        print(f"    Tool Called: {item.tool_name}")
        print(f"    Tool Args: {item.tool_args}")
    if hasattr(item, 'output'):
        print(f"    Tool Output: {item.output}")
from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.tools import function_tool
from openai import AsyncOpenAI
import os

# Gemini client setup
client = AsyncOpenAI(
    api_key="YOUR_GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

@function_tool
def get_weather(city: str) -> str:
    """Gets the current weather for a specified city."""
    if "san francisco" in city.lower():
        return "Sunny and 75 degrees."
    else:
        return "I'm sorry, I don't have the weather for that city."

weather_agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant that can provide weather information.",
    tools=[get_weather],
    model=model
)

result = Runner.run_sync(weather_agent, "What's the weather in San Francisco?")

print(f"Final Output: {result.final_output}")
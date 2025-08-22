from agents import Agent, Runner
from agents.tools import function_tool
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

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
    tools=[get_weather]
)

result = Runner.run_sync(weather_agent, "What's the weather in San Francisco?")

print(f"Final Output: {result.final_output}")
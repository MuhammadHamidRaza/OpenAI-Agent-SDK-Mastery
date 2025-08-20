import asyncio
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
def get_weather(city: str) -> str:
    """Return a short, human-readable weather summary for the given city (mock)."""
    weather_db = {
        "London": "sunny, 20°C",
        "New York": "cloudy, 15°C",
        "Tokyo": "rainy, 18°C",
    }
    return weather_db.get(city, "I don't have weather data for that city.")

agent = Agent(
    name="WeatherBuddy",
    instructions="Use the get_weather tool for live weather queries.",
    tools=[get_weather],
    model=model
)

async def main():
    result = await Runner.run(agent, "What's the weather in London?")
    print(result.final_output)

if __name__ == '__main__':
    asyncio.run(main())

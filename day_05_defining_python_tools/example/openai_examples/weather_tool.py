import asyncio
from agents import Agent, Runner, function_tool

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
)

async def main():
    result = await Runner.run(agent, "What's the weather in London?")
    print(result.final_output)

if __name__ == '__main__':
    asyncio.run(main())

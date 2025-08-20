import asyncio
from agents import Agent, Runner, WebSearchTool, function_tool

@function_tool
def user_preferences(user_id: str) -> str:
    """Fetch stored user preferences for coffee shops.

    Args:
        user_id: Unique user identifier.

    Returns:
        Text description of user's coffee/shop preferences.
        If no preferences are found, returns 'no preferences'.
    """
    prefs = {
        "user_123": "likes quiet places, outdoor seating, medium roast",
        "user_456": "prefers strong espresso, indoor seating, fast service",
        "user_789": "enjoys herbal tea, cozy atmosphere, background music",
    }
    return prefs.get(user_id, "no preferences")

agent = Agent(
    name="CafeFinder",
    instructions=(
        "Help the user choose a coffee shop in San Francisco. "
        "Use WebSearchTool for current weather and shop info, "
        "and incorporate user_preferences(user_id) for personalization."
    ),
    tools=[WebSearchTool(), user_preferences],
)

async def main():
    prompt = (
        "User user_123: Which coffee shop should I go to today in San Francisco, "
        "considering my preferences and today's weather?"
    )
    result = await Runner.run(agent, prompt)
    print("=== Recommendation ===")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
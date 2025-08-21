import asyncio
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# ✅ Gemini client setup
client = AsyncOpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)
@function_tool
def web_search(query: str):
    """
    Performs a web search using Google Custom Search API.

    Args:
        query: The search query.
    Returns:
        List of dictionaries containing title, link, and description.
    """

    API_KEY = "GOOGLE_API_KEY"
    CX = "Search_Engine_Id"
    num_results = 10  # max 10 per request

    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}&num={num_results}"

    response = requests.get(url)
    data = response.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "description": item.get("snippet")
        })
    return results  # ✅ Return a proper list

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
    tools=[web_search, user_preferences],
    model=model
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

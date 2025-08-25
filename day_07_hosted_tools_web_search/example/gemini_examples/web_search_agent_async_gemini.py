import asyncio
import requests
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
from openai import AsyncOpenAI

# ✅ Gemini client setup
client = AsyncOpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
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
    return results

# ✅ Create the agent
agent = Agent(
    name="SearchBuddyAsync",
    instructions="What is Ai.",
    tools=[web_search],
    model=model
)

async def main():
    result = await Runner.run(
        agent, "What are the top headlines about climate technology today?"
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

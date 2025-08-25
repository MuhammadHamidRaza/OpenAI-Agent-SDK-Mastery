import asyncio
from agents import Agent, Runner, SQLiteSession, trace, function_tool, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Gemini client setup
client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

# Optional WebSearchTool (only if available in your env)
# For Gemini, we'll use a custom web_search function as seen in Day 7
import requests

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
    num_results = 10
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

# --- Specialists ---
# Researcher: uses web search when present; otherwise returns concise notes.
researcher = Agent(
    name="Researcher",
    handoff_description="Finds current, credible information from the web (or summarizes known info if web search is unavailable).",
    instructions=(
        "Collect relevant facts, stats, and sources about the user's topic. "
        "If WebSearchTool is available, use it. "
        "Return a short bullet list of key findings and any sources."
    ),
    tools=[web_search], # Using custom web_search function
    model=model
)

# Summarizer: writes a concise paragraph from notes
summarizer = Agent(
    name="Summarizer",
    handoff_description="Turns research notes into a concise, well‑structured paragraph.",
    instructions=(
        "Write a single concise paragraph that synthesizes the Researcher's notes. "
        "Be factual, neutral, and readable for a general audience."
    ),
    model=model
)

# Orchestrator/Planner
orchestrator = Agent(
    name="Planner",
    instructions=(
        "Coordinate specialists. For research tasks, first hand off to Researcher. "
        "Then hand off the notes to Summarizer to produce the final paragraph. "
        "Return the Summarizer's final paragraph to the user."
    ),
    handoffs=[researcher, summarizer],
    model=model
)

async def main():
    session = SQLiteSession(user_id="day12_user", db_path="day12_multi_agent.db")

    with trace(workflow_name="Research & Summarize", group_id="day12"):
        query = "Research the history of AI and write a one‑paragraph summary."
        result = await Runner.run(orchestrator, query, session=session)
        print("\n--- Final Answer ---\n", result.final_output)

        # Follow‑up uses the same session (memory)
        followup = "Great. Add one concise source at the end."
        result2 = await Runner.run(orchestrator, followup, session=session)
        print("\n--- Follow‑up ---\n", result2.final_output)

if __name__ == "__main__":
    asyncio.run(main())
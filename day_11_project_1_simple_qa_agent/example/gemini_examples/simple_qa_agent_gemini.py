import os
import requests
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from agents import function_tool
from openai import AsyncOpenAI

# --- Configuration ---
# Ensure your Gemini API key is set as an environment variable
if "GEMINI_API_KEY" not in os.environ:
    print("Error: GEMINI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()

# ✅ Gemini client setup
client = AsyncOpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", # Using gemini-2.5-flash as per previous corrections
    openai_client=client
)

# --- 1. Initialize the Tool ---
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

web_search_tool = web_search
print("WebSearchTool initialized.")

# --- 2. Define the Agent ---
qa_agent = Agent(
    name="KnowledgeAgent",
    instructions="You are a helpful and knowledgeable assistant. Use the web search tool to find answers to questions. If you cannot find an answer, politely state that you don't know.",
    tools=[web_search_tool],
    model=model # Pass the Gemini model to the agent
)
print("Q&A Agent defined.")

# --- 3. Initialize the Session ---
session = SQLiteSession("user_qa_session", "qa_chat_history.db")
print("SQLiteSession initialized.")

# --- 4. Run the Conversation ---
print("\n--- Starting Q&A Conversation ---")

# First turn
print("\nUser: What is the capital of France?")
result1 = Runner.run_sync(qa_agent, "What is the capital of France?", session=session)
print(f"Agent: {result1.final_output}")

# Second turn, building on context
print("\nUser: And what is its population?")
result2 = Runner.run_sync(qa_agent, "And what is its population?", session=session)
print(f"Agent: {result2.final_output}")

# Third turn, a new question
print("\nUser: Who painted the Mona Lisa?")
result3 = Runner.run_sync(qa_agent, "Who painted the Mona Lisa?", session=session)
print(f"Agent: {result3.final_output}")

print("\n--- Conversation End ---")

# --- 5. Inspect the RunResult ---
print("\n--- Inspecting RunResult for the first turn ---")
print(f"Final Output (Turn 1): {result1.final_output}")
print("Events in Turn 1:")
for item in result1.new_items:
    print(f"  - Type: {type(item).__name__}")
    if hasattr(item, 'text'):
        print(f"    Text: {item.text[:50]}...")
    if hasattr(item, 'tool_name'):
        print(f"    Tool Called: {item.tool_name}")
        print(f"    Tool Args: {item.tool_args}")
    if hasattr(item, 'output'):
        print(f"    Tool Output: {item.output[:50]}...")

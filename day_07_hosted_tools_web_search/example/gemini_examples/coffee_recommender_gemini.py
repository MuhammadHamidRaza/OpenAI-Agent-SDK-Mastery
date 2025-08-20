import asyncio
import google.generativeai as genai
import os
from default_api import google_web_search

# --- Tool Definitions ---

def web_search(query: str):
    """
    Performs a web search using Google Search.

    Args:
        query: The search query.
    """
    print(f"--- Calling Web Search Tool with query: {query} ---")
    return google_web_search(query=query)

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

# --- Agent Setup ---

def create_cafe_finder_agent():
    api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
    if api_key == "YOUR_API_KEY":
        print("Please set the GEMINI_API_KEY environment variable or replace 'YOUR_API_KEY'.")
        return None

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[web_search, user_preferences]
    )
    return model

async def main():
    model = create_cafe_finder_agent()
    if model is None:
        return

    chat = model.start_chat(enable_automatic_function_calling=True)

    prompt = (
        "User user_123: Which coffee shop should I go to today in San Francisco, "
        "considering my preferences and today's weather?"
    )
    print(f"User Prompt: {prompt}\n")

    response = await chat.send_message_async(prompt)

    print("\n=== Recommendation ===")
    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())

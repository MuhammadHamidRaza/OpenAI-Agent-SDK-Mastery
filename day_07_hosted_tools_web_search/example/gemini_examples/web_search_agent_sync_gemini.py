import google.generativeai as genai
import os
from default_api import google_web_search

# --- Tool Definition ---

def web_search(query: str):
    """
    Performs a web search using Google Search.

    Args:
        query: The search query.
    """
    print(f"--- Calling Web Search Tool with query: {query} ---")
    return google_web_search(query=query)

# --- Agent Setup ---

def create_search_agent():
    api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")
    if api_key == "YOUR_API_KEY":
        print("Please set the GEMINI_API_KEY environment variable or replace 'YOUR_API_KEY'.")
        return None

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        tools=[web_search]
    )
    return model

def main():
    model = create_search_agent()
    if model is None:
        return

    chat = model.start_chat(enable_automatic_function_calling=True)

    prompt = "What are the top headlines about climate technology today?"
    print(f"User Prompt: {prompt}\n")

    response = chat.send_message(prompt)

    print("\n--- Final Model Response ---")
    print(response.text)

if __name__ == "__main__":
    main()

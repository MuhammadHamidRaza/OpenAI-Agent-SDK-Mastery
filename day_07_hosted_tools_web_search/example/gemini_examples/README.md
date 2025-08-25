# Gemini Examples - Hosted Tools and Web Search

This directory contains examples demonstrating how to integrate hosted tools, specifically web search, with Gemini models using the `agents` SDK.

## 1. Obtaining Google API Key and Search Engine ID (CX)

To run these examples, you will need a Google API Key and a Custom Search Engine ID (CX). Follow these steps to obtain them:

### How to Obtain `GOOGLE_API_KEY`

1.  **Go to the Google Cloud Console:**
    Open your web browser and navigate to [https://console.cloud.google.com/](https://console.cloud.google.com/).

2.  **Create a New Project (if you don't have one):**
    *   At the top of the page, click on the project dropdown (it usually shows "My First Project" or your current project name).
    *   Click "New Project".
    *   Give your project a name (e.g., "My Search API Project") and click "Create".
    *   Make sure you select this new project once it's created.

3.  **Enable the Custom Search API:**
    *   In the Google Cloud Console, use the navigation menu (three horizontal lines) on the top left.
    *   Go to "APIs & Services" > "Library".
    *   In the search bar, type "Custom Search API" and press Enter.
    *   Click on "Custom Search API" in the search results.
    *   Click the "Enable" button.

4.  **Create API Credentials:**
    *   After enabling the API, go to "APIs & Services" > "Credentials" from the navigation menu.
    *   Click "Create Credentials" at the top and select "API Key".
    *   A new API key will be generated. **Copy this key immediately.** This is your `GOOGLE_API_KEY`.
    *   **Important:** Restrict your API key to prevent unauthorized use. Click "Restrict Key" and select "Custom Search API" under "API restrictions". You can also add "Application restrictions" if you know where your requests will originate from (e.g., IP addresses, HTTP referrers).

### How to Obtain `Search_Engine_Id` (CX)

1.  **Go to the Custom Search Engine Control Panel:**
    Open your web browser and go to [https://programmablesearchengine.google.com/](https://programmablesearchengine.google.com/).

2.  **Create a New Search Engine:**
    *   Click "Add new search engine".
    *   In the "Sites to search" field, you can put `www.google.com` (or leave it to search the entire web if allowed).
    *   Give it a name.
    *   Click "Create".

3.  **Get the Search Engine ID (CX):**
    *   After creating, go to the "Control Panel" for your search engine.
    *   You’ll see "Search engine ID" at the top — this is your CX.
    *   Copy that value; that’s what you use in your code as `CX`.

## 2. Files in this Directory:

### `coffee_recommender_gemini.py`

*   **Purpose:** This script implements a "CafeFinder" agent that recommends coffee shops in San Francisco. It leverages both web search for current weather and shop information, and a custom `user_preferences` tool for personalized recommendations.
*   **Key Concepts Demonstrated:**
    *   **Gemini Model Integration:** Uses `OpenAIChatCompletionsModel` with a Gemini client (`gemini-2.5-flash`).
    *   **Custom Tools:** Defines `web_search` (for Google Custom Search API) and `user_preferences` (a simulated tool to fetch user data). Both are decorated with `@function_tool`.
    *   **Agent Instructions:** The agent's instructions guide it to use the available tools for a specific task (coffee shop recommendation).
    *   **Asynchronous Execution:** The `main` function uses `asyncio.run` to execute the agent asynchronously.
*   **How it Works:** The agent receives a prompt including a user ID. It then uses the `user_preferences` tool to get the user's coffee preferences and the `web_search` tool to find information about coffee shops and potentially weather. Based on this information, it provides a recommendation.
*   **Setup:** Requires `GOOGLE_API_KEY` and `Search_Engine_Id` for the `web_search` tool, and `GEMINI_API_KEY` for the Gemini model.

### `web_search_agent_async_gemini.py`

*   **Purpose:** This script demonstrates an asynchronous agent that performs web searches using the Google Custom Search API.
*   **Key Concepts Demonstrated:**
    *   **Asynchronous Agent Execution:** The agent is run using `Runner.run`, which is an asynchronous call.
    *   **Gemini Model Integration:** Similar to `coffee_recommender_gemini.py`, it uses `OpenAIChatCompletionsModel` with a Gemini client (`gemini-2.5-flash`).
    *   **Web Search Tool:** Defines a `web_search` tool using `@function_tool` to interact with the Google Custom Search API.
*   **How it Works:** The agent is given a prompt (e.g., "What are the top headlines about climate technology today?"). It then uses the `web_search` tool to find relevant information and returns the `final_output`.
*   **Setup:** Requires `GOOGLE_API_KEY`, `Search_Engine_Id`, and `GEMINI_API_KEY`.

### `web_search_agent_sync_gemini.py`

*   **Purpose:** This script demonstrates a synchronous agent that performs web searches using the Google Custom Search API. It is functionally similar to `web_search_agent_async_gemini.py` but uses a synchronous execution model.
*   **Key Concepts Demonstrated:**
    *   **Synchronous Agent Execution:** The agent is run using `Runner.run_sync`, which is a blocking call.
    *   **Gemini Model Integration:** Uses `OpenAIChatCompletionsModel` with a Gemini client (`gemini-2.5-flash`). Note the different model version compared to the async example.
    *   **Web Search Tool:** Defines the same `web_search` tool as in the asynchronous example.
*   **How it Works:** The agent receives a prompt, uses the `web_search` tool to gather information, and provides a `final_output`. The execution is blocking until the result is obtained.
*   **Setup:** Requires `GOOGLE_API_KEY`, `Search_Engine_Id`, and `GEMINI_API_KEY`.

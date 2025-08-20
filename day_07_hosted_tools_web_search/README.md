
# Day 7 — Hosted Tools: Web Search

## Course Overview

Welcome to Day 7 of **OpenAI Agent SDK Mastery**. Today we cover **hosted tools** — provider-hosted, server-side tools that run alongside the LLM — and focus on **web search**. Hosted tools let agents fetch live facts, query stored documents, run sandboxed code, or generate images without you building the backend for each capability.

### TL;DR

-   Hosted tools run on the provider side and enable live capabilities (web search, code execution, retrieval, image generation, etc.).
    
-   The `WebSearchTool` is a common hosted tool for fetching up-to-date web information.
    
-   Combine hosted tools with local function-tools (personalization, DB access) and guardrails for safety and privacy.
    
-   If hosted tools aren’t available in your account/region, mock them in development and enable them in staging.
    

----------

## Objectives

After this lesson, you will:

1.  Understand what hosted tools are and why they matter.
    
2.  Recognize the main hosted tools the SDK offers.
    
3.  Attach a hosted `WebSearchTool` to an agent and run it (async & sync examples).
    
4.  Combine hosted and local tools in a real-world pattern (coffee-shop recommender).
    
5.  Test with mocks and follow best practices for safety and availability.
    

----------

## 1) Hosted Tools — What & Why

Hosted tools are pre-built functions provided by the **OpenAI Agents platform/provider** and executed on the provider’s servers. They let agents perform real-time operations without you hosting integrations.

### Why use hosted tools?

-   **Immediate access to live data & features**
    
-   **Less infrastructure to build and maintain**
    
-   **Provider-managed scaling, quotas, and sometimes safety checks**
    

----------

## 2) Key Hosted Tools (Common Set)

> Exact availability and names can vary by SDK version/account — check your SDK docs if unsure.

-   `WebSearchTool` — search the live web for facts, news, pages, snippets.
    
-   `FileSearchTool` — query content in your OpenAI Vector Stores / uploaded files.
    
-   `ComputerTool` — controlled automation / sandboxed computer tasks.
    
-   `CodeInterpreterTool` — run sandboxed code for computation, file processing, charts, etc.
    
-   `HostedMCPTool` — expose a remote MCP server’s tools to the model.
    
-   `ImageGenerationTool` — generate images from prompts.
    
-   `LocalShellTool` — runs shell commands locally on your machine (**not hosted**; be careful with permissions & security).
    

> **Note:** Most tools above are provider-hosted. Always confirm tool availability in your docs and account.

----------

## 3) How Hosted Tools Fit into the Agent Loop

**Flow:**

```
User prompt → LLM decides it needs live info → LLM emits a structured tool call 
→ SDK runs hosted tool → tool returns results → LLM finalizes reply
```

----------

## 4) Minimal WebSearch Usage — Async Example

```python
# web_search_agent_async.py
import asyncio
from agents import WebSearchTool

from agents import Agent, Runner

agent = Agent(
    name="SearchBuddy",
    instructions="Answer user questions using web search when needed.",
    tools=[WebSearchTool()],
)

async def main():
    result = await Runner.run(agent, "What's the latest news about artificial intelligence?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```
**Notes:**

-   Hosted tool availability may require enabling in your OpenAI account.
    
-   Some hosted tools call external provider APIs — you may need provider keys configured in environment variables.
    

----------

## 5) Minimal WebSearch Usage — Sync Example
```python
# web_search_agent_sync.py
from agents import WebSearchTool
from agents import Agent, Runner

agent = Agent(
    name="SearchBuddySync",
    instructions="Answer user questions using web search when needed.",
    tools=[WebSearchTool()],
)

# Blocking call for simple scripts
result = Runner.run_sync(agent, "What are the top headlines about climate technology today?")
print(result.final_output)

```
----------

## 6) Real-World Example — Coffee-Shop Recommender

Combines **hosted `WebSearchTool`** (for weather & reviews) with a **local personalization function**. Production-style code with docstrings and type hints.

```python
# coffee_recommender.py
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

```

**How it works:**

1.  Model determines it needs current weather and top shops → calls `WebSearchTool`.
    
2.  Model obtains preferences via `user_preferences(user_id="user_123")`.
    
3.  SDK executes both tools and returns outputs to the model, which composes a final recommendation.
    

----------

## 7) Offline Testing & Mocking Hosted Tools

When hosted tools aren’t available in dev/CI environments:

```python
from agents import function_tool, Agent, Runner

@function_tool
def mock_web_search(query: str) -> str:
    """Mocked web search for unit tests."""
    return f"[MOCK SEARCH] Results for: {query}"

agent = Agent(name="MockSearchAgent", instructions="Use mock...", tools=[mock_web_search])
result = Runner.run_sync(agent, "List recent events in X")
print(result.final_output)

```

**Tip:**

-   Use mocks for tests and enable hosted tools only in integration/staging.
    
-   Ensures safe, reliable testing even without real API calls.
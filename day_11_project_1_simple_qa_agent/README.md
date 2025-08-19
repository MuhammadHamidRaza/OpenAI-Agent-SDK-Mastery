# Day 11: Project 1: Simple Q&A Agent

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 11 of the **OpenAI Agent SDK Mastery** course! After ten days of building foundational knowledge—from understanding agents and their execution to defining tools, managing memory, and observing behavior through tracing—it's time to synthesize these concepts into your first complete project. Today, you will build a **Simple Q&A Agent**. This project will solidify your understanding of how different components of the OpenAI Agents SDK work together to create a functional and intelligent application. You'll define an agent, equip it with a tool for information retrieval, and ensure it can maintain context across turns using sessions, all while being able to trace its operations for debugging.

---

## Project Goal: Build a Simple Q&A Agent

Your goal for today is to create an agent that can answer general knowledge questions. To make it truly useful, it should be able to:

1.  **Answer questions** by leveraging an external information source (e.g., web search).
2.  **Maintain conversation context** across multiple turns.
3.  Allow for **observability** of its internal workings.

### Components We'll Use:

*   **Agent:** The core intelligent entity.
*   **`WebSearchTool`:** To fetch up-to-date information (as discussed on Day 7).
*   **`SQLiteSession`:** To manage conversational memory (as discussed on Day 2 and Day 8).
*   **`Runner`:** To execute the agent (as discussed on Day 3).
*   **Tracing/`RunResult`:** To inspect the agent's behavior (as discussed on Day 9 and Day 10).

---

## Step-by-Step Implementation

### Step 1: Setup and Tool Definition

First, ensure your environment is set up with your OpenAI API key. We'll define the `WebSearchTool`. Remember that for `WebSearchTool`, you might need additional API keys for the underlying search service (e.g., Google Custom Search API).

```python
import os
from agents import Agent, Runner, SQLiteSession
from agents.tools import WebSearchTool # Assuming this is available and configured

# ---
# Configuration ---
# Ensure your OpenAI API key is set as an environment variable
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()

# If using WebSearchTool that requires Google API Key and CSE ID
# if "GOOGLE_API_KEY" not in os.environ or "GOOGLE_CSE_ID" not in os.environ:
#     print("Warning: GOOGLE_API_KEY or GOOGLE_CSE_ID not set. WebSearchTool might not function.")
#     # You might want to exit or handle this gracefully based on your needs

# Initialize the WebSearchTool
# Note: The actual initialization might vary based on your SDK version and search backend.
# For demonstration, we assume a basic initialization.
web_search_tool = WebSearchTool()

print("Setup complete and WebSearchTool initialized.")
```

### Step 2: Define Your Q&A Agent

Now, create your `Agent` instance. Provide clear instructions and pass the `web_search_tool` to it.

```python
# ... (previous code for imports and setup) ...

qa_agent = Agent(
    name="KnowledgeAgent",
    instructions="You are a helpful and knowledgeable assistant. Use the web search tool to find answers to questions. If you cannot find an answer, politely state that you don't know.",
    tools=[web_search_tool] # Provide the web search tool to the agent
)

print("Q&A Agent defined with WebSearchTool.")
```

### Step 3: Implement Conversational Memory with `SQLiteSession`

To make the agent remember past interactions, we'll use `SQLiteSession`. This will allow for multi-turn conversations.

```python
# ... (previous code for imports, setup, and agent definition) ...

# Initialize a session. You can use a unique session ID for each user or conversation.
# The database file 'qa_chat_history.db' will be created/used in the current directory.
session = SQLiteSession("user_qa_session", "qa_chat_history.db")

print("SQLiteSession initialized for conversational memory.")
```

### Step 4: Run the Agent and Test Conversational Flow

Now, let's run the agent with a few questions, demonstrating how it uses the tool and remembers context.

```python
# ... (previous code for imports, setup, agent definition, and session initialization) ...

print("\n--- Starting Q&A Conversation ---")

# First turn
print("\nUser: What is the capital of France?")
result1 = Runner.run_sync(qa_agent, "What is the capital of France?", session=session)
print(f"Agent: {result1.final_output}")

# Second turn, building on context (agent should remember the previous topic)
print("\nUser: And what is its population?")
result2 = Runner.run_sync(qa_agent, "And what is its population?", session=session)
print(f"Agent: {result2.final_output}")

# Third turn, a new question
print("\nUser: Who painted the Mona Lisa?")
result3 = Runner.run_sync(qa_agent, "Who painted the Mona Lisa?", session=session)
print(f"Agent: {result3.final_output}")

print("\n--- Conversation End ---")

# Optional: Clear the session if you want to start fresh for next run
# session.clear_session()
# print("Session cleared.")
```

### Step 5: Observe with Tracing (Optional but Recommended)

To see how the agent makes decisions and uses the tool, you can inspect the `RunResult` objects. This is crucial for debugging and understanding.

```python
# ... (previous code for imports, setup, agent definition, session initialization, and conversation) ...

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

print("\n--- Inspecting RunResult for the second turn ---")
print(f"Final Output (Turn 2): {result2.final_output}")
print("Events in Turn 2:")
for item in result2.new_items:
    print(f"  - Type: {type(item).__name__}")
    if hasattr(item, 'text'):
        print(f"    Text: {item.text[:50]}...")
    if hasattr(item, 'tool_name'):
        print(f"    Tool Called: {item.tool_name}")
        print(f"    Tool Args: {item.tool_args}")
    if hasattr(item, 'output'):
        print(f"    Tool Output: {item.output[:50]}...")

```

---

## Key Takeaways from Project 1

*   You've successfully built your first complete AI agent, integrating multiple core concepts of the OpenAI Agents SDK.
*   The `WebSearchTool` allows your agent to access dynamic, real-time information, overcoming the LLM's knowledge cut-off.
*   `SQLiteSession` provides persistent conversational memory, enabling natural, multi-turn interactions.
*   Inspecting `RunResult` objects and their `new_items` property is crucial for understanding and debugging your agent's decision-making process.
*   This project demonstrates the power of combining agents with tools and memory to create truly intelligent and useful applications.

Congratulations on completing your first project! This is a significant milestone in your journey to mastering the OpenAI Agents SDK. Tomorrow, we'll begin exploring **Multi-Agent Systems**, understanding how multiple agents can collaborate to solve even more complex problems.
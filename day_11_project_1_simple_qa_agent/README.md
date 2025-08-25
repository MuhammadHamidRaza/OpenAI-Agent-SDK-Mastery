# Day 11: Project 1: Simple Q&A Agent

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 11 of the **OpenAI Agent SDK Mastery** course! After ten days of building foundational knowledge—from understanding agents and their execution to defining tools, managing memory, and observing behavior through tracing—it's time to synthesize these concepts into your first complete project. Today, you will build a **Simple Q&A Agent**. This project will solidify your understanding of how different components of the OpenAI Agents SDK work together to create a functional and intelligent application.

---

### **TL;DR**

*   Combine `Agent`, `WebSearchTool`, `SQLiteSession`, and `Runner` to build a conversational Q&A agent.
*   Use `WebSearchTool` to give the agent access to real-time information.
*   Use `SQLiteSession` to maintain conversation history.
*   Inspect `RunResult` to understand the agent's behavior.

---

### **Objectives**

*   Build a complete Q&A agent from scratch.
*   Integrate a hosted tool (`WebSearchTool`) with an agent.
*   Implement conversational memory using `SQLiteSession`.
*   Run and test a multi-turn conversation with an agent.
*   Inspect the agent's execution flow using `RunResult`.

---

## 1) Project Goal: Build a Simple Q&A Agent

Your goal for today is to create an agent that can answer general knowledge questions. To make it truly useful, it should be able to:

1.  **Answer questions** by leveraging an external information source (e.g., web search).
2.  **Maintain conversation context** across multiple turns.
3.  Allow for **observability** of its internal workings.

---

## 2) Components We'll Use

*   **Agent:** The core intelligent entity.
*   **`WebSearchTool`:** To fetch up-to-date information.
*   **`SQLiteSession`:** To manage conversational memory.
*   **`Runner`:** To execute the agent.
*   **Tracing/`RunResult`:** To inspect the agent's behavior.

---

## 3) Step-by-Step Implementation

Here is the complete code for the Simple Q&A Agent.

```python
import os
from agents import Agent, Runner, SQLiteSession
from agents import WebSearchTool

# ---
# Configuration ---
# Ensure your OpenAI API key is set as an environment variable
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()


# ---
# 1. Define the Agent ---
qa_agent = Agent(
    name="KnowledgeAgent",
    instructions="You are a helpful and knowledgeable assistant. Use the web search tool to find answers to questions. If you cannot find an answer, politely state that you don't know.",
    tools=[WebSearchTool()]
)
print("Q&A Agent defined.")

# ---
# 2. Initialize the Session ---
# The database file 'qa_chat_history.db' will be created/used in the current directory.
session = SQLiteSession("user_qa_session", "qa_chat_history.db")
print("SQLiteSession initialized.")

# ---
# 4. Run the Conversation ---
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

# ---
# 5. Inspect the RunResult ---
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

```

---

## 4) How it Works

1.  **Configuration:** The code first checks for the `OPENAI_API_KEY` environment variable.
2.  **Tool Initialization:** It initializes the `WebSearchTool`, which will be used by the agent to search the web.
3.  **Agent Definition:** An `Agent` is created with a name, instructions, and the `WebSearchTool`. The instructions guide the agent on how to behave and when to use the tool.
4.  **Session Initialization:** A `SQLiteSession` is created to store the conversation history. This allows the agent to remember previous turns.
5.  **Conversation Execution:** The `Runner.run_sync()` method is used to execute the agent for each turn of the conversation. The `session` object is passed to the runner to maintain context.
6.  **RunResult Inspection:** After the conversation, the `RunResult` object from the first turn is inspected to show the events that occurred during the agent's execution, including the tool call.

---

## 5) Key Takeaways from Project 1

*   You've successfully built your first complete AI agent, integrating multiple core concepts of the OpenAI Agents SDK.
*   The `WebSearchTool` allows your agent to access dynamic, real-time information, overcoming the LLM's knowledge cut-off.
*   `SQLiteSession` provides persistent conversational memory, enabling natural, multi-turn interactions.
*   Inspecting `RunResult` objects and their `new_items` property is crucial for understanding and debugging your agent's decision-making process.
*   This project demonstrates the power of combining agents with tools and memory to create truly intelligent and useful applications.

Congratulations on completing your first project! This is a significant milestone in your journey to mastering the OpenAI Agents SDK. Tomorrow, we'll begin exploring **Multi-Agent Systems**, understanding how multiple agents can collaborate to solve even more complex problems.

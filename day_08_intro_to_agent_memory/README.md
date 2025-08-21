# Day 8 — Intro to Agent Memory

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

## **Course Overview**

Welcome to Day 8 of the **OpenAI Agent SDK Mastery** course! Today, we'll explore the critical concept of **Agent Memory**. You'll learn why agents need to remember information, the difference between short-term and long-term memory, and how to implement both using the Agents SDK. By the end of this lesson, you'll be able to build more intelligent and context-aware agents that can maintain conversations and recall important facts across sessions.

---

### TL;DR

*   **Short-term memory (Session):** Manages conversation context for a single chat. Use `SQLiteSession` to maintain the current thread's history for follow-up questions.
*   **Long-term memory (Persistent):** Saves facts across different runs (e.g., in a database or JSON file). You can retrieve these facts and inject them into the agent's prompt.
*   Use **Sessions** for a better multi-turn user experience, and be mindful of privacy by only persisting necessary information.

----------

### Objectives

After this lesson, you will:

1.  Understand the difference between short-term and long-term agent memory.
2.  Use `SQLiteSession` to manage conversational history.
3.  Implement a simple long-term memory solution using a JSON file.
4.  Know the best practices for managing agent memory, including data privacy and token usage.

----------

## 1) Why Memory Matters

LLMs are stateless by default, meaning each interaction is independent. To create natural, multi-turn conversations, you must provide the context of previous messages. Memory gives agents:

*   **Conversational Continuity:** Allows for follow-up questions and a natural flow of conversation.
*   **Personalization:** Enables the agent to remember user preferences and tailor its responses.
*   **Multi-step Task Capability:** Allows the agent to build on previous work and complete complex tasks over multiple interactions.

----------

## 2) Short-term vs. Long-term Memory

Here’s a quick comparison:

| Feature      | Short-term (Session)                      | Long-term (Persistent)                     |
|--------------|-------------------------------------------|--------------------------------------------|
| **Lifetime** | Current conversation/session              | Across sessions, days, or months           |
| **Storage**  | In-memory or session DB (`SQLiteSession`) | DB, file, vector store, or external store  |
| **Use case** | Follow-ups, clarifications, active tasks  | User profiles, order history, knowledge base |
| **Token cost** | Adds to prompt (consumes tokens)        | Fetch & inject relevant facts (controlled) |

----------

## 3) Sessions for Short-term Memory

When you pass a `session` object to the `Runner`, the SDK automatically handles the conversation history. It will:

1.  Fetch the session history (previous turns).
2.  Include that history in the prompt so the model has context.
3.  Run the agent.
4.  Append the newly generated messages to the session.

> **Note:** The exact import path for `SQLiteSession` can vary by SDK version. If `from agents import SQLiteSession` fails, try `from agents.session.sqlite import SQLiteSession` or consult the SDK documentation.

----------

## 4) Code Examples

Minimal imports & setup (common to all examples)
# Use this for sync examples
from agents import Agent, Runner, SQLiteSession
# Use asyncio + Runner.run(...) for async examples
import asyncio

1) Short-term Session — Sync (temporary, in-memory for this process)
# day08_short_sync.py
from agents import Agent, Runner, SQLiteSession

agent = Agent(name="MemoryAssistant", instructions="Reply concisely.")

# Temporary session (in-memory for this program run)
session = SQLiteSession("conversation_temp")

# Turn 1: store a fact in the session
res1 = Runner.run_sync(agent, "Hi — my name is Sara and I like pizza.", session=session)
print("Turn 1:", res1.final_output)

# Turn 2: follow-up uses session history automatically
res2 = Runner.run_sync(agent, "What's my name?", session=session)
print("Turn 2:", res2.final_output)  # Expect "Sara"


When to use: chat UI, single conversation thread, tests.

2) Persistent Session — Sync (saved between program runs)
# day08_persistent_sync.py
from agents import Agent, Runner, SQLiteSession

agent = Agent(name="PersistentAssistant", instructions="Remember user facts across runs.")

# Persistent session saved to conversations.db
persistent_session = SQLiteSession("user_123", "conversations.db")

# Save a persistent fact
Runner.run_sync(persistent_session, "Note: favorite_drink=chai")  # optional helper run to add items
Runner.run_sync(agent, "Remember: my favorite drink is chai.", session=persistent_session)

# Later (after restarting the program), this will still be remembered:
res = Runner.run_sync(agent, "What is my favorite drink?", session=persistent_session)
print(res.final_output)  # Should mention "chai"


When to use: user profiles, support tickets, any memory you want kept across restarts.

Note: Some SDKs let you call session.add_items(...) directly — use that if you want to programmatically add items instead of using the agent runs.

3) Short-term Session — Async
# day08_short_async.py
import asyncio
from agents import Agent, Runner, SQLiteSession

async def main():
    agent = Agent(name="AsyncMemoryBot", instructions="Be friendly.")
    session = SQLiteSession("async_session_1")
    await Runner.run(agent, "My name is Alex.", session=session)
    result = await Runner.run(agent, "What is my name?", session=session)
    print(result.final_output)  # Expects "Alex"

if __name__ == "__main__":
    asyncio.run(main())

4) Memory operations (async) — get_items, add_items, pop_item, clear_session
# day08_memory_ops.py
import asyncio
from agents import SQLiteSession

async def demo():
    session = SQLiteSession("memory_ops", "test.db")

    # Add items (programmatically)
    new_items = [
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi there! How can I help?"}
    ]
    await session.add_items(new_items)
    print("Added conversation items.")

    # Read items
    items = await session.get_items()
    print(f"Memory contains {len(items)} items.")
    for i in items[-5:]:
        print(i)

    # Pop last item (undo)
    last = await session.pop_item()
    print("Removed last item:", last)

    # Clear session
    await session.clear_session()
    print("Cleared session. Items now:", await session.get_items())

asyncio.run(demo())

5) Using pop_item() for corrections (undo last assistant+user)
# day08_correction.py
import asyncio
from agents import Agent, Runner, SQLiteSession

async def main():
    agent = Agent(name="Calc", instructions="Answer math questions simply.")
    session = SQLiteSession("correction_example")

    # initial wrong question/answer
    await Runner.run(agent, "What's 2 + 2?", session=session)
    print("Initial answer saved.")

    # Remove assistant response and user's question (undo)
    await session.pop_item()  # removes assistant's last message
    await session.pop_item()  # removes user's last message

    # Ask corrected question
    res = await Runner.run(agent, "What's 2 + 3?", session=session)
    print("Corrected answer:", res.final_output)

asyncio.run(main())

6) Long-term facts pattern (external store + injection) — recommended for controlled token use

Instead of appending huge histories, keep selective persistent facts and inject them into the prompt.

# day08_longterm_inject.py
from agents import Agent, Runner

agent = Agent(name="LongTermAgent", instructions="Use known user facts where relevant.")

# Simulated long-term store (could be DB / JSON / vector store)
long_term_store = {
    "user_42": {"favorite_drink": "chai", "city": "Karachi"}
}

# Before running, fetch facts and inject a compact context snippet:
facts = long_term_store.get("user_42", {})
pref_text = f"User facts: favorite_drink={facts.get('favorite_drink','unknown')}, city={facts.get('city','unknown')}\n"

result = Runner.run_sync(agent, f"{pref_text}\nUser: Recommend a coffee shop nearby.")
print(result.final_output)


Why this pattern: keeps token usage small, lets you control what persistent info is shown, and is easy to combine with Sessions.

7) Small real-world pattern — Customer Support (per-user sessions)
```python
# day08_support_bot.py
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

class SupportBot:
    def __init__(self):
        # Gemini client setup
        self.client = AsyncOpenAI(
            api_key="GEMINI_API_KEY",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Gemini model
        self.model = OpenAIChatCompletionsModel(
            model="gemini-2.5-flash",
            openai_client=self.client
        )

        self.agent = Agent(
            name="SupportBot",
            instructions="You are a helpful customer support agent. Be polite and remember conversation history for each user.",
            model=self.model
        )

    def session_for(self, customer_id: str):
        return SQLiteSession(f"customer_{customer_id}", "support_conversations.db")

    async def chat(self, customer_id: str, message: str):
        session = self.session_for(customer_id)
        result = await Runner.run(self.agent, message, session=session)
        return result.final_output

# Usage
async def main():
    bot = SupportBot()
    print(await bot.chat("123", "Hi, I'm having trouble with order #12345"))
    print(await bot.chat("123", "What was my order number again?"))  # should recall #12345
    print(await bot.chat("456", "Hello, I need help with billing"))  # separate conversation

if __name__ == "__main__":
    asyncio.run(main())
```

8) Custom Session implementation (stub)

If you need Redis / Postgres / remote storage, implement the Session protocol:

# day08_custom_session.py
from typing import List
from agents.memory import Session  # protocol interface

class MyCustomSession(Session):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._items = []

    async def get_items(self, limit: int | None = None) -> List[dict]:
        return self._items[-limit:] if limit else list(self._items)

    async def add_items(self, items: List[dict]) -> None:
        self._items.extend(items)

    async def pop_item(self) -> dict | None:
        return self._items.pop() if self._items else None

    async def clear_session(self) -> None:
        self._items.clear()



----------

## 5) Memory Operations (Common Session APIs)

Here are some common session methods you might use:

*   `await session.get_items(limit=None)`: Read stored items from the session (async).
*   `await session.add_items(items)`: Programmatically add items to the session.
*   `await session.pop_item()`: Remove the last item (useful for "undo" functionality).
*   `await session.clear_session()`: Delete the history for the current session.

> **Note:** The exact method names may vary slightly by SDK version. Check your installed SDK's documentation if you encounter an API error.

----------

## 6) Real-World Patterns

*   **Customer Support:**
    *   **Short-term:** The current support ticket conversation.
    *   **Long-term:** The customer's order history and past support tickets.
*   **Educational Tutor:**
    *   **Short-term:** The context of the current lesson.
    *   **Long-term:** The student's performance profile and learning history.
*   **Personal Assistant:**
    *   **Short-term:** The details of the itinerary being planned.
    *   **Long-term:** The user's travel preferences (e.g., hotel type, dietary needs).

----------

## 7) Best Practices & Pitfalls

*   **Scope Sessions Well:** Use meaningful `session_id`s (e.g., `user_123`, `ticket_456`) to prevent conversations from getting mixed up.
*   **Trim & Summarize:** To save tokens on long conversations, consider summarizing older turns instead of sending the full history every time.
*   **Persist Only What You Need:** Avoid storing sensitive personal information unless necessary. Use encryption and set data retention policies.
*   **Limit Retrieval Size:** For very long histories, fetch only the last N items or a summary.
*   **Test Undo Flows:** Use `pop_item()` to allow users to correct the agent gracefully.

----------

## 8) Short Exercises

1.  **Session Test:** Run the short-term sync example and confirm that the follow-up question correctly uses the saved name.
2.  **Persistence Test:** Run the persistent session example, stop the script, then re-run it to confirm the agent still remembers the fact.
3.  **Hybrid Test:** Save a fact in both a `SQLiteSession` and the `long_term_memory.json` file. Create a run that uses both the JSON facts and the session context to answer a query.

----------

## 9) Quick Checklist

*   Ensure you have Python 3.8+ and an active virtual environment.
*   Install the appropriate Agents SDK (e.g., `pip install openai-agents`).
*   Check the SDK documentation for the correct import path for `SQLiteSession` if you encounter errors.
*   Do not store sensitive personal information in plain text.

----------

## Summary

Short-term sessions (`SQLiteSession`) provide conversational continuity, which is ideal for chat-based user experiences. Long-term persistence (e.g., a database or JSON file) allows your agent to remember facts across multiple sessions and provide personalized suggestions. For the best results, combine both: use a **Session** for the active conversation and selectively fetch and inject long-term facts when they are relevant.

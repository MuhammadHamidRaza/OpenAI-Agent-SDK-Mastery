# Day 8: Intro to Agent Memory

## Key Concepts:

- **Agent Memory:** The ability of an agent to retain information across conversational turns.
- **Short-term Memory (Session):** Managed by `SQLiteSession` to keep track of the current conversation's context.
- **Long-term Memory (Persistent):** Storing facts across sessions, for example in a JSON file or a database.
- **Memory Management:** Using session methods like `get_items()`, `clear()`, and `pop_item()`.

## Examples:

Refer to the `example/` directory for code examples demonstrating:
- Synchronous and asynchronous sessions.
- Persistent sessions using a database file.
- A simple long-term memory implementation with JSON.

## Notes / Tips:

- Use meaningful `session_id`s to keep conversations separate.
- Be mindful of privacy and token costs when managing memory.
- For long conversations, consider summarizing older parts of the history.

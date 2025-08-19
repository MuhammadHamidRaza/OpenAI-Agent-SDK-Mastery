# Day 35: SDK Configuration & `RunConfig`

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 35 of the **OpenAI Agent SDK Mastery** course! We've covered a wide range of topics, from agent fundamentals to advanced memory and multi-agent systems. Today, we revisit and deepen our understanding of **SDK Configuration**, with a specific focus on the `RunConfig` object (or similar mechanisms) that provides granular control over individual agent executions. While you've seen basic configuration on Day 15, this session will empower you to master fine-tuning the behavior of your agents for specific scenarios, optimizing performance, cost, and output quality on a per-run basis. By the end of today, you'll be able to precisely control how your agents operate in diverse contexts.

---

## The Need for Granular Control: Why `RunConfig`?

In many real-world applications, a single agent might need to behave differently depending on the user's query, the current system load, or specific business requirements. For example:

*   A customer support agent might need to be highly creative for initial greetings but very precise when providing technical solutions.
*   A research agent might need to prioritize speed for quick lookups but thoroughness for in-depth reports.
*   You might want to test different LLM models or temperature settings for specific prompts without changing the agent's default configuration.

While `Agent` objects can have default `ModelSettings`, `RunConfig` (or similar per-run configuration objects) allows you to override these defaults dynamically for a single `Runner.run()` call. This provides immense flexibility and control.

---

## Understanding `RunConfig` (or Equivalent Parameters)

The `Runner.run()`, `Runner.run_sync()`, and `Runner.run_streamed()` methods typically accept parameters that allow you to configure the behavior of that specific run. These parameters often encapsulate what might be found in a dedicated `RunConfig` object in some SDKs. Common configurable aspects include:

1.  **`model_settings`**:
    *   **`model`**: Override the default LLM model (e.g., `gpt-3.5-turbo`, `gpt-4`).
    *   **`temperature`**: Control the randomness/creativity of the LLM's output (0.0 for deterministic, higher for more creative).
    *   **`max_tokens`**: Limit the maximum number of tokens in the LLM's response.
    *   **`top_p`, `frequency_penalty`, `presence_penalty`**: Advanced LLM generation parameters.
2.  **`max_turns`**: Limit the number of internal turns the agent can take to reach a final answer, preventing infinite loops.
3.  **`session`**: Specify a particular session to use for the run, overriding any default session associated with the agent.
4.  **`tools`**: Provide a specific set of tools for that run, potentially overriding the agent's default tools. This is useful for context-specific tool access.
5.  **`guardrails`**: Apply specific input or output guardrails for that particular run.
6.  **`callbacks`**: Attach custom callback functions to monitor the run's progress or events.

---

## Practical Examples of `RunConfig` Usage

### Example 1: Overriding Model Settings for Creativity

Let's use the same agent but make it more creative for one specific response.

```python
from agents import Agent, Runner, ModelSettings
import os

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define a general-purpose agent with default (low creativity) settings
default_agent = Agent(
    name="DefaultAssistant",
    instructions="You are a helpful and factual assistant.",
    model_settings=ModelSettings(temperature=0.2) # Default to low creativity
)

print("--- Testing Model Setting Overrides ---")

# Run with default settings
print("\nQuery 1 (Default Temperature): Write a short story about a robot.")
result1 = Runner.run_sync(default_agent, "Write a short story about a robot.")
print(f"Agent (Default): {result1.final_output}")

# Run with higher temperature for more creativity
print("\nQuery 2 (High Temperature): Write a short story about a robot.")
result2 = Runner.run_sync(
    default_agent,
    "Write a short story about a robot.",
    model_settings=ModelSettings(temperature=0.8) # Override for this run
)
print(f"Agent (Creative): {result2.final_output}")

```

**Explanation:**

*   The `default_agent` is initialized with `temperature=0.2`.
*   For `result2`, we pass a new `ModelSettings` object to `Runner.run_sync()`, overriding the `temperature` to `0.8` for that specific call. The agent itself remains configured with `0.2` for subsequent calls unless overridden again.

### Example 2: Limiting `max_turns` for a Specific Run

Prevent an agent from taking too many turns for a particular query.

```python
# ... (imports and setup) ...

loopy_agent = Agent(
    name="LoopyAssistant",
    instructions="You are an assistant that always asks a follow-up question to gather more details."
)

print("\n--- Testing Max Turns Override ---")

# Run without max_turns limit (might go on for a while conceptually)
# print("\nQuery 1 (No Max Turns): Tell me about your favorite hobby.")
# result1 = Runner.run_sync(loopy_agent, "Tell me about your favorite hobby.")
# print(f"Agent: {result1.final_output}")

# Run with a strict max_turns limit
print("\nQuery 2 (Max Turns = 2): Tell me about your favorite hobby.")
try:
    result2 = Runner.run_sync(loopy_agent, "Tell me about your favorite hobby.", max_turns=2)
    print(f"Agent: {result2.final_output}")
except Exception as e:
    print(f"Agent encountered an error (expected MaxTurnsExceeded): {e}")

```

**Explanation:**

*   The `loopy_agent` is designed to ask follow-up questions, potentially leading to many turns.
*   By setting `max_turns=2` in the `Runner.run_sync()` call, we explicitly limit the agent's internal loop for that specific interaction, ensuring it doesn't run indefinitely.

### Example 3: Providing Context-Specific Tools

An agent might have a default set of tools, but for a specific query, you might want to provide an additional, temporary tool.

```python
# ... (imports and setup) ...
from agents.tools import function_tool

@function_tool
def get_special_info(topic: str) -> str:
    """Retrieves highly specialized information about a given topic."""
    if topic.lower() == "quantum physics":
        return "Quantum physics studies matter and energy at the most fundamental level."
    return "No special info for that topic."

# Agent without get_special_info by default
general_agent = Agent(
    name="GeneralAssistant",
    instructions="You are a general knowledge assistant."
)

print("\n--- Testing Context-Specific Tools ---")

# Query without the special tool
print("\nQuery 1 (No Special Tool): Tell me about quantum physics.")
result1 = Runner.run_sync(general_agent, "Tell me about quantum physics.")
print(f"Agent: {result1.final_output}")

# Query with the special tool provided for this run
print("\nQuery 2 (With Special Tool): Tell me about quantum physics.")
result2 = Runner.run_sync(
    general_agent,
    "Tell me about quantum physics.",
    tools=[get_special_info] # Provide tool for this run only
)
print(f"Agent: {result2.final_output}")

```

**Explanation:**

*   The `general_agent` doesn't have `get_special_info` by default.
*   For `result2`, we pass `tools=[get_special_info]` to `Runner.run_sync()`, making that tool available *only* for that specific execution. The agent can then use it if its instructions and the prompt warrant it.

---

## Key Takeaways

*   **SDK Configuration** and the `RunConfig` (or equivalent parameters in `Runner.run()` methods) provide **granular control** over individual agent executions.
*   You can dynamically override default `ModelSettings` (e.g., `model`, `temperature`, `max_tokens`), `max_turns`, `session`, and even the `tools` available for a specific run.
*   This flexibility is crucial for optimizing agents for diverse scenarios, A/B testing, and fine-tuning behavior without altering the agent's core definition.
*   Mastering `RunConfig` empowers you to precisely control your agent's behavior in real-world applications.

Today, you've gained mastery over fine-tuning your agent's behavior on a per-run basis. Tomorrow, we'll apply this and other concepts to build **Realtime Agents Implementation**, creating low-latency agents for live chat scenarios.
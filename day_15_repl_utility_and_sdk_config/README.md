# Day 15: REPL Utility and SDK Configuration

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 15 of the **OpenAI Agent SDK Mastery** course! Today marks the conclusion of our first level, where we've built a strong foundation in agent fundamentals. To round out your toolkit, we'll explore two practical aspects that significantly enhance your development workflow: the **REPL (Read-Eval-Print Loop) Utility** and **SDK Configuration**. The REPL provides an interactive environment for quickly testing agent behaviors and tool interactions, while understanding SDK configuration allows you to customize the behavior of your agents and the underlying models. Mastering these will make your agent development process more efficient and flexible.

---

## The REPL Utility: Interactive Agent Development

A REPL (Read-Eval-Print Loop) is an interactive programming environment that takes single user inputs (or sets of inputs), evaluates them, and returns the result to the user. It's an invaluable tool for rapid prototyping, testing, and debugging, especially when working with AI agents.

While the OpenAI Agents SDK might not provide a dedicated, standalone REPL application, the concept applies to how you can interactively test your agents within a Python interpreter or an IDE's interactive console (like Jupyter notebooks or IPython).

### Benefits of using a REPL for Agent Development:

*   **Rapid Prototyping:** Quickly test agent instructions, tool definitions, and prompt variations without needing to run an entire script.
*   **Interactive Debugging:** Step through agent interactions, inspect `RunResult` objects, and modify variables on the fly.
*   **Experimentation:** Easily experiment with different agent behaviors, tool outputs, and session management.
*   **Learning:** A great way to understand how the SDK components interact by trying out small snippets of code.

### How to use it (Conceptual):

You can simply open a Python interpreter in your terminal and import your agent components.

```python
# In your terminal, type 'python' or 'ipython'
# >>> from agents import Agent, Runner
# >>> from agents.tools import function_tool
# >>> import os

# >>> # Assume your API key is set
# >>> # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# >>> @function_tool
# >>> def multiply(a: float, b: float) -> float:
# >>>     """Multiplies two numbers."""
# >>>     return a * b

# >>> my_agent = Agent(
# >>>     name="MathAgent",
# >>>     instructions="You are a math assistant.",
# >>>     tools=[multiply]
# >>> )

# >>> result = Runner.run_sync(my_agent, "What is 5 times 7?")
# >>> print(result.final_output)
# 35

# >>> result2 = Runner.run_sync(my_agent, "Can you multiply 10 by 3.5?")
# >>> print(result2.final_output)
# 35.0

print("The REPL allows for quick, interactive testing of agents and tools.")
print("Simply run your Python interpreter and import your agent components.")
```

---

## SDK Configuration: Customizing Agent Behavior

The OpenAI Agents SDK provides various configuration options that allow you to fine-tune the behavior of your agents, control the underlying LLMs, and manage resources. These configurations can often be set globally, per agent, or even per `Runner` execution.

### Common Configuration Areas:

1.  **LLM Model Selection:** Choosing which specific LLM model to use (e.g., `gpt-4`, `gpt-3.5-turbo`). This impacts cost, performance, and capabilities.
2.  **Model Parameters:** Adjusting parameters like `temperature` (creativity vs. determinism), `max_tokens` (response length), and `top_p`.
3.  **Max Turns:** Limiting the number of turns an agent can take in its internal loop to prevent infinite loops or excessive resource consumption.
4.  **Tool Configuration:** Specific settings for built-in tools (e.g., API keys for `WebSearchTool`).
5.  **Session Management:** Configuring where session data is stored (e.g., database path for `SQLiteSession`).

### How to Configure (Conceptual):

Configuration is typically done through parameters in `Agent` or `Runner` constructors, or via a dedicated `ModelSettings` object.

```python
from agents import Agent, Runner, ModelSettings
import os

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# 1. Global/Default Model Settings (Conceptual)
# You might set default model settings that apply to all agents unless overridden.
# from agents import set_default_model_settings
# set_default_model_settings(ModelSettings(model="gpt-4-turbo", temperature=0.7))

# 2. Agent-Specific Model Settings
# You can pass ModelSettings directly to the Agent constructor.
creative_agent = Agent(
    name="Poet",
    instructions="You are a creative poet.",
    model_settings=ModelSettings(temperature=0.9, model="gpt-3.5-turbo")
)

# 3. Runner-Specific Overrides
# You can override settings for a specific run using the Runner.
# This is useful for one-off tests or dynamic adjustments.
print("Running creative agent with default settings...")
result1 = Runner.run_sync(creative_agent, "Write a short poem about a lonely cloud.")
print(f"Agent 1: {result1.final_output}")

print("\nRunning creative agent with lower temperature for more deterministic output...")
result2 = Runner.run_sync(
    creative_agent,
    "Write a short poem about a lonely cloud.",
    model_settings=ModelSettings(temperature=0.2) # Override for this run
)
print(f"Agent 2: {result2.final_output}")

# 4. Max Turns Configuration
# You can limit the number of turns an agent takes to prevent infinite loops.
loopy_agent = Agent(
    name="Loopy",
    instructions="Always ask a follow-up question."
)

try:
    print("\nRunning loopy agent with max_turns=3...")
    result3 = Runner.run_sync(loopy_agent, "Tell me about yourself.", max_turns=3)
    print(f"Agent 3: {result3.final_output}")
except Exception as e:
    print(f"Agent 3 encountered an error: {e}") # Likely MaxTurnsExceeded

print("SDK configuration provides fine-grained control over agent behavior.")
```

---

## Key Takeaways

*   The **REPL utility** (interactive Python interpreter) is an excellent environment for rapid prototyping, testing, and debugging of agents and tools.
*   **SDK Configuration** allows you to customize various aspects of your agent's behavior, including LLM model selection, model parameters (`temperature`, `max_tokens`), and execution limits (`max_turns`).
*   Configuration can often be applied globally, per agent, or overridden for individual `Runner` executions, providing flexibility.
*   Mastering these practical aspects will significantly improve your efficiency and control over agent development.

Congratulations! You've completed the first level of the **OpenAI Agent SDK Mastery** course. You now have a solid understanding of agent fundamentals, including execution, tools, memory, tracing, and basic configuration. Get ready for Level 2, where we'll dive into more advanced topics and complex projects!
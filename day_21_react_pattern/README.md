# Day 21: `ReAct` Pattern: Reasoning and Acting

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 21 of the **OpenAI Agent SDK Mastery** course! We've explored agent planning, where agents can autonomously devise a sequence of actions. Today, we delve into a highly influential and effective pattern for building intelligent agents: the **ReAct (Reasoning and Acting) pattern**. ReAct combines the strengths of Chain-of-Thought (CoT) prompting with the ability to interact with external environments through tools. Agents following the ReAct pattern iteratively generate thoughts, perform actions, and observe the results, allowing them to dynamically adapt, gather information, and solve complex problems. This session will provide a deep dive into the ReAct loop and its practical implications for agent design.

---

## The Genesis of ReAct: Combining Reasoning and Action

Traditional LLM prompting often involves either generating a direct answer or a chain of thought. However, for tasks requiring interaction with external tools or dynamic environments, a more iterative approach is needed. The ReAct pattern, introduced in the paper "ReAct: Synergizing Reasoning and Acting in Language Models," addresses this by integrating explicit reasoning steps with external actions.

### Why ReAct is Powerful:

*   **Dynamic Adaptation:** Agents can adjust their plan based on observations from the environment or tool outputs.
*   **Error Recovery:** If an action fails or yields unexpected results, the agent can reason about the error and attempt a different approach.
*   **Information Gathering:** Agents can use tools to gather necessary information before making decisions or generating final answers.
*   **Transparency:** The explicit "Thought" steps provide a clear trace of the agent's decision-making process, aiding in debugging and understanding.
*   **Complex Problem Solving:** Enables agents to tackle multi-step problems that require both internal reasoning and external interaction.

---

## The ReAct Loop: Thought, Action, Observation

The core of the ReAct pattern is an iterative loop that cycles through three distinct phases:

1.  **Thought (Reasoning):** The agent's internal monologue. The LLM generates a thought process, explaining its current understanding of the problem, what it needs to do next, and why. This is where the planning and strategic thinking occur.
2.  **Action (Acting):** Based on its thought, the agent decides to perform an action. This typically involves calling an external tool with specific arguments (e.g., a web search, a calculator, an API call).
3.  **Observation (Observing):** The agent receives the result of its action. This observation (e.g., the output of a tool, an error message) provides new information that the agent incorporates into its context for the next iteration of the loop.

This cycle continues until the agent determines it has achieved its goal and can provide a final answer.

### Visualizing the ReAct Loop:

```
User Query
    |
    V
[Thought] -> What do I need to do? What tool should I use?
    |
    V
[Action] -> Call Tool(arguments)
    |
    V
[Observation] -> Tool Output / Environment Feedback
    |
    V
(Loop back to Thought, or if goal achieved, generate Final Answer)
```

---

## Implementing ReAct in the OpenAI Agents SDK

The OpenAI Agents SDK inherently supports the ReAct pattern. When you provide an agent with tools and clear instructions, the underlying LLM, especially powerful models like GPT-4, will naturally adopt a ReAct-like behavior if prompted correctly. The SDK's `Runner` and `RunResult` (with its `new_items` containing `ToolCallItem`, `ToolCallOutputItem`, and potentially `ReasoningItem`) facilitate this loop.

To encourage ReAct behavior, your agent's instructions should guide the LLM to:

*   Explicitly state its thoughts.
*   Identify when a tool is needed.
*   Use the tool.
*   Process the tool's output.

### Example: Agent Demonstrating ReAct Behavior

Let's create an agent that uses a web search tool and explicitly shows its thought process.

```python
from agents import Agent, Runner
from agents.tools import WebSearchTool # Assuming this is available
import os

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Assume WebSearchTool is configured
web_search_tool = WebSearchTool()

react_agent = Agent(
    name="ReActAssistant",
    instructions=(
        "You are a helpful assistant that follows the ReAct pattern. "
        "Always think step-by-step before taking an action. "
        "Your response should always start with 'Thought:' followed by your reasoning, "
        "then 'Action:' if you are calling a tool, and 'Observation:' after a tool's output. "
        "Finally, provide a concise 'Answer:'. "
        "Available tools: WebSearchTool for finding information."
    ),
    tools=[web_search_tool]
)

print("Running ReActAssistant...")
query = "What is the capital of Canada and its current population?"
result = Runner.run_sync(react_agent, query)

print(f"\nAgent's final output: {result.final_output}")

print("\n--- Detailed ReAct Trace (from new_items) ---")
for item in result.new_items:
    print(f"Type: {type(item).__name__}")
    if hasattr(item, 'text'):
        print(f"  Text: {item.text}")
    if hasattr(item, 'tool_name'):
        print(f"  Tool Call: {item.tool_name}({item.tool_args})")
    if hasattr(item, 'output'):
        print(f"  Tool Output: {item.output}")
    print("---")

```

**Explanation:**

*   The `react_agent`'s instructions explicitly guide the LLM to output its `Thought`, `Action`, and `Observation` steps. This makes the ReAct process transparent.
*   The `Runner.run_sync` executes the agent, and the `new_items` in the `RunResult` will contain the sequence of these steps, including the `ToolCallItem` and `ToolCallOutputItem` for the `WebSearchTool`.

---

## Key Takeaways

*   The **ReAct pattern** combines explicit reasoning (`Thought`) with external interaction (`Action`) and feedback (`Observation`) in an iterative loop.
*   It significantly enhances an agent's ability to adapt, recover from errors, gather information, and solve complex, multi-step problems.
*   The OpenAI Agents SDK naturally supports ReAct behavior, especially when agents are provided with clear instructions to verbalize their thought process and use tools.
*   Tracing (Day 10) and inspecting `RunResult.new_items` (Day 9) are crucial for understanding and debugging ReAct-based agents.

Today, you've gained a deep understanding of a powerful agentic pattern. Tomorrow, you'll apply this and all previous knowledge to your second major project: building an **Automated Research Assistant**, which will heavily leverage tools and iterative reasoning.
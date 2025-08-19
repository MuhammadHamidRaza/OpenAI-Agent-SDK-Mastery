# Day 20: Agent Planning

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 20 of the **OpenAI Agent SDK Mastery** course! We've explored how to orchestrate multi-agent workflows by explicitly defining the sequence of tasks. Today, we delve into a more advanced and autonomous capability: **Agent Planning**. Instead of following a pre-defined script, an agent with planning capabilities can autonomously break down a complex problem into smaller, manageable steps, decide which tools to use, and determine the optimal sequence of actions to achieve a goal. This session will introduce the concept of agent planning, its benefits, and the underlying techniques that enable agents to generate their own solutions, making them significantly more adaptable and intelligent.

---

## What is Agent Planning?

**Agent planning** refers to an agent's ability to generate a sequence of actions or sub-goals to achieve a given objective. Unlike explicit orchestration (where the developer defines the workflow), planning allows the agent to dynamically construct its own strategy based on the problem description, its available tools, and its current state.

Think of it as the difference between following a recipe (orchestration) and a chef creating a new dish from scratch based on available ingredients and desired taste (planning).

### Why is Agent Planning Important?

*   **Adaptability:** Agents can handle novel or unforeseen problems without requiring explicit programming for every scenario.
*   **Autonomy:** Reduces the need for human intervention in defining complex workflows.
*   **Efficiency:** Can find optimal or near-optimal paths to a solution.
*   **Robustness:** Can recover from errors or unexpected outcomes by replanning.
*   **Complex Problem Solving:** Enables agents to tackle highly complex, multi-step problems that are difficult to hardcode.

---

## How Agents Plan (Conceptual Approaches)

Agent planning often leverages the reasoning capabilities of Large Language Models (LLMs) to generate and refine plans. Here are some conceptual approaches:

### 1. Chain-of-Thought (CoT)

*   **Description:** The LLM is prompted to generate intermediate reasoning steps before providing a final answer or action. This makes the LLM's thought process explicit and can improve its ability to solve complex problems.
*   **How it aids planning:** By explicitly thinking step-by-step, the LLM can outline a plan before executing it. Each step in the chain can be a sub-goal or a decision point.
*   **Example Prompt Idea:** "Let's think step by step. First, I need to... Then, I will... Finally, I should..."

### 2. Tree-of-Thought (ToT)

*   **Description:** Extends Chain-of-Thought by exploring multiple reasoning paths (a tree structure) and evaluating them. The agent can backtrack if a path leads to a dead end or a suboptimal solution.
*   **How it aids planning:** Allows for more robust planning by considering alternatives and selecting the best path, similar to how humans might brainstorm and evaluate options.

### 3. Tool-Use Planning

*   **Description:** The agent's planning process is tightly integrated with its available tools. The LLM decides which tool to use, when, and with what arguments, as part of its overall plan.
*   **How it aids planning:** The LLM generates a sequence of tool calls to achieve a goal. This is often seen in agents that can use a variety of external functions.

### 4. Goal-Oriented Planning

*   **Description:** The agent is given a high-level goal and uses its knowledge and tools to recursively break down the goal into smaller sub-goals until they are actionable.
*   **How it aids planning:** Focuses on achieving the end state, allowing the agent to dynamically figure out the intermediate steps.

---

## Implementing Planning in the OpenAI Agents SDK (Conceptual)

While the OpenAI Agents SDK provides the primitives (Agents, Tools, Runner) that enable planning, the planning logic itself is often driven by the LLM's instructions and the way you structure your prompts. The SDK facilitates the execution of the plan (e.g., by executing tool calls suggested by the LLM).

To encourage planning, you can:

*   **Provide Clear Instructions:** Instruct the agent to "think step-by-step," "create a plan before acting," or "break down the problem."
*   **Define Tools with Clear Descriptions:** The LLM needs to understand what each tool does to incorporate it into a plan.
*   **Iterative Prompting:** In some cases, you might prompt the agent to generate a plan, then review it, and then prompt it to execute the plan.

### Example: Agent with Simple Planning Instruction

Let's create an agent that is instructed to plan its approach before answering a complex question.

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

planner_agent = Agent(
    name="PlannerAgent",
    instructions=(
        "You are a problem-solving assistant. For any complex query, first, outline a step-by-step plan to address it. "
        "Then, execute the plan using your available tools and provide the final answer. "
        "Available tools: WebSearchTool for finding information."
    ),
    tools=[web_search_tool]
)

print("Running PlannerAgent with a complex query...")
query = "Research the history of artificial intelligence, focusing on key milestones and influential figures, and then summarize it."
result = Runner.run_sync(planner_agent, query)

print(f"\nAgent's final output: {result.final_output}")

print("\n--- Inspecting Agent's Thought Process (Conceptual) ---")
# In a real scenario, you would inspect result.new_items for ReasoningItem or similar
# to see the generated plan and execution steps.
for item in result.new_items:
    if hasattr(item, 'text'):
        # This might contain the planning steps if the LLM outputs them as text
        print(f"  Message: {item.text[:100]}...")
    if hasattr(item, 'tool_name'):
        print(f"  Tool Call: {item.tool_name}({item.tool_args})")
    if hasattr(item, 'output'):
        print(f"  Tool Output: {item.output[:100]}...")

```

**Explanation:**

*   The `PlannerAgent`'s instructions explicitly tell it to "first, outline a step-by-step plan" and then "execute the plan." This encourages the LLM to engage in a planning phase.
*   The `Runner.run_sync` call will execute the agent. If the LLM successfully plans, its internal thought process (which might be visible in `new_items` as `ReasoningItem` or just as part of the `MessageOutputItem` if the LLM verbalizes its plan) would show the generated steps.

---

## Key Takeaways

*   **Agent Planning** enables agents to autonomously break down problems and generate their own sequence of actions.
*   It enhances adaptability, autonomy, and robustness for complex problem-solving.
*   Techniques like Chain-of-Thought and Tool-Use Planning leverage the LLM's reasoning capabilities.
*   You can encourage planning by providing clear instructions to the agent to outline its steps before acting.
*   Tracing (Day 10) is crucial for observing and debugging an agent's planning process.

Today, you've gained insight into how agents can become more proactive problem-solvers. Tomorrow, we'll delve deeper into a specific planning pattern: the **ReAct Pattern**, which combines reasoning and acting in an iterative loop.
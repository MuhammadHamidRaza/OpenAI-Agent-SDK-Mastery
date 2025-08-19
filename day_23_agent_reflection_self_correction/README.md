# Day 23: Agent Reflection & Self-Correction

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 23 of the **OpenAI Agent SDK Mastery** course! You've built agents that can plan and collaborate. Today, we introduce a crucial capability that elevates agent intelligence to a new level: **Agent Reflection and Self-Correction**. Just as humans learn from their mistakes and refine their approaches, advanced AI agents can be designed to critically evaluate their own outputs, identify shortcomings, and then adjust their strategies or re-attempt tasks. This session will explore the principles behind reflection, its importance for robustness and performance, and how to implement internal feedback loops that enable your agents to learn and improve autonomously.

---

## The Importance of Reflection for Agents

Even with sophisticated planning and tool use, agents can sometimes produce suboptimal or incorrect outputs due to:

*   **Misinterpretation of Prompts:** The LLM might misunderstand the user's true intent.
*   **Tool Misuse:** Incorrect arguments passed to a tool, or misinterpretation of tool output.
*   **Incomplete Information:** Lack of sufficient data to provide a comprehensive answer.
*   **Logical Errors:** Flaws in the LLM's reasoning process.
*   **Hallucinations:** Generating factually incorrect but plausible-sounding information.

**Reflection** is the process by which an agent critically examines its own work. **Self-correction** is the subsequent action taken to rectify any identified issues. This internal feedback loop is vital for:

*   **Increased Accuracy:** Agents can catch and fix their own errors.
*   **Enhanced Robustness:** Agents become more resilient to unexpected inputs or complex scenarios.
*   **Improved Performance:** Over time, agents can learn to produce better quality outputs.
*   **Reduced Human Oversight:** Less need for constant human intervention to correct agent behavior.

---

## How Agent Reflection Works (Conceptual)

Agent reflection typically involves a meta-cognitive loop where the agent (or a dedicated "critic" agent) evaluates a generated output or a sequence of actions against a set of criteria or a desired outcome. This process often leverages the LLM's ability to reason about its own work.

### Common Reflection Mechanisms:

1.  **Self-Critique:** The agent is prompted to review its own answer or plan and identify potential flaws, missing information, or areas for improvement.
2.  **Critique by Another Agent:** In a multi-agent system, a dedicated "critic" or "evaluator" agent assesses the output of another agent.
3.  **Comparison to Ground Truth/Criteria:** The agent compares its output against known facts, predefined rules, or specific quality metrics.
4.  **Error Analysis:** If a tool call fails or an unexpected observation occurs, the agent reflects on the error message to understand the cause and devise a recovery strategy.

### The Reflection-Correction Loop:

```
User Query -> Agent Generates Output/Plan
    |
    V
[Reflection] -> Evaluate Output/Plan against criteria. Identify issues.
    |
    V
(If issues found) -> [Self-Correction] -> Revise Output/Plan / Re-attempt Task
    |
    V
(If no issues or after correction) -> Final Output
```

---

## Implementing Reflection and Self-Correction

Implementing reflection often involves structuring your prompts or agent workflows to include a review phase. You can instruct the LLM to act as a critic of its own work.

### Example: Agent with Self-Correction for Factual Accuracy

Let's create an agent that attempts to answer a question, then reflects on its answer, and if it finds a potential issue (e.g., a lack of specific detail), it uses a tool to correct or enhance its response.

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

# Agent that answers and then reflects
reflective_agent = Agent(
    name="ReflectiveAssistant",
    instructions=(
        "You are a helpful assistant. First, try to answer the user's question directly. "
        "Then, critically review your own answer for accuracy, completeness, and clarity. "
        "If you find any shortcomings or need more detail, use the WebSearchTool to improve your answer. "
        "Finally, provide the best possible answer. "
        "Available tools: WebSearchTool for finding information."
    ),
    tools=[web_search_tool]
)

print("Running ReflectiveAssistant...")
query = "Who was the first person to walk on the moon?"
result = Runner.run_sync(reflective_agent, query)

print(f"\nAgent's final output: {result.final_output}")

print("\n--- Inspecting Agent's Reflection Process (Conceptual) ---")
# You would typically look for specific patterns in the new_items or LLM messages
# that indicate reflection and self-correction steps.
for item in result.new_items:
    if hasattr(item, 'text'):
        # Look for phrases like "Thought: I need to check..." or "Critique: My previous answer..."
        print(f"  Message: {item.text[:100]}...")
    if hasattr(item, 'tool_name'):
        print(f"  Tool Call: {item.tool_name}({item.tool_args})")
    if hasattr(item, 'output'):
        print(f"  Tool Output: {item.output[:100]}...")

```

**Explanation:**

*   The `reflective_agent`'s instructions explicitly guide it to first answer, then "critically review" its own answer, and then "use the WebSearchTool to improve" if needed.
*   The LLM, when following these instructions, will likely generate internal thoughts that represent the reflection process. If it identifies a need for more information, it will then trigger the `WebSearchTool`.
*   The `new_items` in the `RunResult` would show this iterative process: initial answer attempt, then a tool call for research, then a refined answer.

---

## Key Considerations for Reflection

*   **Cost:** Each reflection step involves additional LLM calls, which can increase latency and cost. Use reflection judiciously for tasks where accuracy and robustness are critical.
*   **Criteria for Reflection:** Clearly define what constitutes a "good" or "bad" answer for the agent to evaluate against. This can be part of the instructions or external rules.
*   **Iterative Refinement:** Reflection can be a single step or an iterative process where the agent refines its answer over several turns until it meets the criteria.
*   **Human Feedback:** While agents can self-correct, human feedback remains invaluable for training and improving reflection mechanisms over time.

---

## Key Takeaways

*   **Agent Reflection** is the ability of an agent to critically evaluate its own outputs or actions.
*   **Self-Correction** is the subsequent process of revising or re-attempting a task based on that evaluation.
*   This internal feedback loop significantly enhances an agent's **accuracy, robustness, and autonomy**.
*   You can implement reflection by carefully crafting agent instructions that prompt the LLM to critique its own work and use tools for improvement.
*   Reflection adds complexity and cost but is invaluable for high-stakes or complex problem-solving scenarios.

Today, you've empowered your agents to become more self-aware and capable of continuous improvement. Tomorrow, we'll shift our focus to another critical aspect of agent robustness: **Input & Output Validation Guardrails**, ensuring your agents operate within safe and defined parameters.
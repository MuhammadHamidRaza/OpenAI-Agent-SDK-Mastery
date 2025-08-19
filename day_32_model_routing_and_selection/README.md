# Day 32: Model Routing and Selection

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 32 of the **OpenAI Agent SDK Mastery** course! You've built agents that can use tools, remember, and even speak. Today, we introduce a sophisticated optimization technique: **Model Routing and Selection**. As the landscape of Large Language Models (LLMs) expands, with models varying in cost, speed, and specialized capabilities, it becomes inefficient to use a single, often expensive, LLM for all tasks. Model routing involves intelligently directing a user's query to the most appropriate LLM based on factors like query complexity, type, or specific requirements. This session will explore the rationale behind dynamic model selection and how to implement a system that automatically routes queries to optimize for cost, performance, and accuracy.

---

## Why Dynamic Model Routing?

Using a single, powerful (and often expensive) LLM like GPT-4 for every single query can be inefficient. Consider the diversity of tasks an agent might handle:

*   A simple greeting vs. a complex coding problem.
*   A factual lookup vs. a creative writing task.
*   A quick, low-stakes question vs. a critical decision-making query.

Different LLMs excel at different tasks and come with varying trade-offs:

*   **Cost:** Smaller, faster models (e.g., `gpt-3.5-turbo`) are significantly cheaper than larger, more capable ones (e.g., `gpt-4`).
*   **Latency:** Simpler models generally respond faster.
*   **Capability:** Some models are better at reasoning, others at creative generation, and some are fine-tuned for specific domains.
*   **Context Window:** Models vary in how much context they can handle.

**Dynamic Model Routing** allows you to leverage the strengths of multiple LLMs, optimizing for:

*   **Cost-Efficiency:** Use cheaper models for simpler tasks.
*   **Performance:** Route to faster models for latency-sensitive interactions.
*   **Accuracy/Quality:** Select the most capable model for complex or critical tasks.
*   **Specialization:** Direct queries to models fine-tuned for specific domains.

---

## How Model Routing Works (Conceptual)

Model routing typically involves an initial decision-making layer that analyzes the incoming query and determines which LLM is best suited to handle it. This decision can be based on various criteria:

1.  **Keyword/Pattern Matching:** Simple rules based on keywords in the query (e.g., "code" -> `coding_model`, "weather" -> `weather_model`).
2.  **Query Complexity Analysis:** Using a smaller LLM or a heuristic to assess the complexity of the query (e.g., "Is this a simple question or a complex reasoning task?").
3.  **Intent Classification:** Classifying the user's intent (e.g., "summarize," "generate code," "answer factual question") and routing to a model specialized for that intent.
4.  **Tool Requirements:** If the query implies the need for a specific tool, route to an agent/model that has access to that tool.
5.  **Confidence Scores:** If multiple models can answer, choose the one with the highest confidence score (if available).

### Conceptual Routing Flow:

```
User Query
    |
    V
[Router Agent / Logic] -> Analyze Query
    |
    V
(Decision) -> Route to:
    |
    +--- [Simple LLM (e.g., gpt-3.5-turbo)] for simple Q&A, greetings
    |
    +--- [Complex LLM (e.g., gpt-4)] for reasoning, complex problem-solving
    |
    +--- [Specialized LLM (e.g., fine-tuned code model)] for code generation
    |
    +--- [Creative LLM] for content generation
    |
    V
Agent Response
```

---

## Implementing Model Routing in the OpenAI Agents SDK

The OpenAI Agents SDK allows you to specify the LLM model for an agent via `ModelSettings`. To implement routing, you would typically have a primary agent or a custom function that acts as the router. This router would analyze the input and then dynamically select which `Agent` instance (configured with a specific `ModelSettings`) to run.

### Example: Simple Model Router Agent

Let's create a router agent that directs queries to a cheaper model for simple questions and a more expensive model for complex ones.

```python
from agents import Agent, Runner, ModelSettings
import os

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define agents with different model settings
simple_agent = Agent(
    name="SimpleResponder",
    instructions="You are a quick and concise assistant for simple questions.",
    model_settings=ModelSettings(model="gpt-3.5-turbo", temperature=0.2) # Cheaper, faster
)

complex_agent = Agent(
    name="ComplexSolver",
    instructions="You are a highly intelligent and thorough assistant for complex reasoning tasks.",
    model_settings=ModelSettings(model="gpt-4", temperature=0.7) # More capable, expensive
)

# A router agent or function to decide which agent to use
router_agent = Agent(
    name="Router",
    instructions=(
        "You are a routing agent. Your task is to determine if a user's query is simple or complex. "
        "If it's a simple factual question or a greeting, indicate 'simple'. "
        "If it requires deep reasoning, problem-solving, or creative generation, indicate 'complex'. "
        "Respond with only the word 'simple' or 'complex'."
    ),
    model_settings=ModelSettings(model="gpt-3.5-turbo", temperature=0.0) # Use a cheap, deterministic model for routing
)

def route_and_run(query: str) -> str:
    print(f"\nRouting query: '{query}'")
    # Use the router agent to classify the query
    routing_decision_result = Runner.run_sync(router_agent, f"Is this query simple or complex? Query: {query}")
    decision = routing_decision_result.final_output.strip().lower()

    if "simple" in decision:
        print("Decision: Routing to SimpleResponder.")
        final_result = Runner.run_sync(simple_agent, query)
    elif "complex" in decision:
        print("Decision: Routing to ComplexSolver.")
        final_result = Runner.run_sync(complex_agent, query)
    else:
        print("Decision: Could not classify, defaulting to SimpleResponder.")
        final_result = Runner.run_sync(simple_agent, query)
    
    return final_result.final_output

print("--- Testing Model Routing ---")

# Test simple query
response1 = route_and_run("Hello, how are you?")
print(f"Final Response: {response1}")

# Test complex query
response2 = route_and_run("Explain the theory of relativity in simple terms.")
print(f"Final Response: {response2}")

# Test another simple query
response3 = route_and_run("What is 2 + 2?")
print(f"Final Response: {response3}")

# Test another complex query
response4 = route_and_run("Design a Python function that calculates the Fibonacci sequence up to n terms.")
print(f"Final Response: {response4}")

```

**Explanation:**

*   We define two agents, `simple_agent` and `complex_agent`, each configured with a different LLM model.
*   A `router_agent` (a lightweight LLM) is used to classify the incoming query as "simple" or "complex."
*   The `route_and_run` function then uses this classification to decide which specialized agent to execute.

---

## Key Considerations for Model Routing

*   **Routing Accuracy:** The effectiveness of your router agent is critical. Poor routing can lead to incorrect answers or wasted resources.
*   **Overhead:** The routing decision itself adds a small amount of latency and cost. Ensure the benefits outweigh this overhead.
*   **Fallback Mechanisms:** Have a default model or a strategy for queries that cannot be confidently routed.
*   **Monitoring:** Track which models are being used for which types of queries to refine your routing logic.
*   **Dynamic Configuration:** Consider externalizing model configurations and routing rules for easier updates.

---

## Key Takeaways

*   **Model Routing and Selection** allows you to dynamically choose the most appropriate LLM for a given query.
*   This optimizes for **cost, performance, and accuracy** by leveraging the strengths of different models.
*   Routing can be based on query complexity, intent, keywords, or tool requirements.
*   You can implement routing by using a lightweight LLM as a classifier to direct queries to specialized agents configured with different models.

Today, you've learned how to make your agent systems more efficient and intelligent by dynamically selecting the right tool for the job. Tomorrow, we'll explore **Caching Strategies**, another powerful technique to reduce latency and lower costs for frequently accessed queries.
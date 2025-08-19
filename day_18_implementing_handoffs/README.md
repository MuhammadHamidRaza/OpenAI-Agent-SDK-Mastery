# Day 18: Implementing `Handoffs`

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 18 of the **OpenAI Agent SDK Mastery** course! We've discussed the theory of Multi-Agent Systems and the concept of Handoffs. Today, we bring that theory to life by **implementing handoffs** in a practical scenario. You'll learn how to define multiple specialized agents and orchestrate a workflow where one agent intelligently delegates a task to another. This hands-on session will solidify your understanding of inter-agent communication, a cornerstone of building complex, collaborative AI systems. By the end of today, you'll be able to design and implement agent teams that work together seamlessly to solve problems.

---

## Recap: Why Handoffs?

As we learned on Day 12 and 13, handoffs are crucial for:

*   **Specialization:** Allowing agents to focus on their core expertise.
*   **Modularity:** Breaking down complex problems into manageable parts.
*   **Scalability:** Developing and deploying agents independently.
*   **Efficiency:** Ensuring tasks are handled by the most capable agent.

The OpenAI Agents SDK simplifies the process of defining and executing these handoffs, making multi-agent orchestration accessible.

---

## The `Handoff` Primitive in OpenAI Agents SDK

The SDK provides a dedicated mechanism for handoffs. Typically, an agent, based on its instructions and the current context, will decide to initiate a handoff. This involves specifying the target agent and passing relevant information.

### Key Steps in Implementing Handoffs:

1.  **Define Specialized Agents:** Create individual `Agent` instances, each with distinct instructions and potentially unique tools, representing different areas of expertise.
2.  **Orchestrator/Router Agent:** Design an initial agent (often called a router or orchestrator) whose primary role is to understand the user's intent and decide which specialist agent should handle the request.
3.  **Handoff Instruction:** The orchestrator agent's instructions should guide it to identify when a handoff is needed and to which agent.
4.  **Executing the Handoff:** The SDK handles the underlying mechanics of transferring control and context when the LLM decides to perform a handoff.

---

## Practical Scenario: Customer Support Triage

Let's build a simplified customer support system where an initial `TriageAgent` directs user queries to either a `BillingAgent` or a `TechnicalSupportAgent`.

### Agents Involved:

*   **`TriageAgent`:** The first point of contact. Its job is to understand the user's problem and hand it off to the correct specialist.
*   **`BillingAgent`:** Handles queries related to invoices, payments, and subscriptions.
*   **`TechnicalSupportAgent`:** Handles queries related to product functionality, bugs, and troubleshooting.

```python
from agents import Agent, Runner, Handoff
import os

# Ensure the OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()

# 1. Define the Specialized Agents

billing_agent = Agent(
    name="BillingAgent",
    instructions="You are a billing specialist. You handle all inquiries related to invoices, payments, and subscriptions. Provide clear and concise answers regarding billing matters."
)

tech_support_agent = Agent(
    name="TechnicalSupportAgent",
    instructions="You are a technical support specialist. You assist users with product functionality, troubleshooting, and bug reports. Provide step-by-step solutions or direct them to relevant documentation."
)

# 2. Define the Triage Agent (Orchestrator)
# This agent needs to know about the other agents to hand off to them.
# The SDK's Handoff primitive allows the LLM to select the target agent.

triage_agent = Agent(
    name="TriageAgent",
    instructions=(
        "You are a customer support triage agent. Your role is to understand the user's problem "
        "and hand off the conversation to the appropriate specialist agent: "
        "'BillingAgent' for billing or payment issues, or 'TechnicalSupportAgent' for product or technical issues. "
        "Do not try to answer the question yourself; only hand off."
    ),
    # The SDK automatically makes other defined agents available for handoff if they are in scope
    # or explicitly passed. For simplicity, the LLM's instructions guide the handoff.
)

# 3. Run the Triage Agent and Observe Handoffs

print("--- Starting Customer Support Triage Simulation ---")

# Scenario 1: Billing Inquiry
user_query_1 = "I have a question about my last invoice. It seems incorrect."
print(f"\nUser: {user_query_1}")

# When running the triage_agent, the SDK will manage the handoff if the LLM decides to do so.
# The Runner will automatically activate the target agent.
result1 = Runner.run_sync(triage_agent, user_query_1)

print(f"Agent's final response (after potential handoff): {result1.final_output}")
print(f"Handled by: {result1.last_agent.name}")

# Scenario 2: Technical Issue
user_query_2 = "My software is crashing every time I try to open a file. Can you help?"
print(f"\nUser: {user_query_2}")
result2 = Runner.run_sync(triage_agent, user_query_2)

print(f"Agent's final response (after potential handoff): {result2.final_output}")
print(f"Handled by: {result2.last_agent.name}")

# Scenario 3: Ambiguous Query (might default to one or ask for clarification)
user_query_3 = "I need help with my account."
print(f"\nUser: {user_query_3}")
result3 = Runner.run_sync(triage_agent, user_query_3)

print(f"Agent's final response (after potential handoff): {result3.final_output}")
print(f"Handled by: {result3.last_agent.name}")

print("--- Simulation End ---")

```

**Explanation:**

*   We define `BillingAgent` and `TechnicalSupportAgent` with their specific instructions.
*   The `TriageAgent` is instructed to *only* hand off to these specialists. Its instructions are crucial for guiding the LLM's decision-making process.
*   When `Runner.run_sync()` is called with `triage_agent`, the LLM within `triage_agent` analyzes the user query. If it determines that a specialist is needed, it will generate a `Handoff` call.
*   The SDK intercepts this `Handoff` call and automatically transfers control to the specified target agent (`BillingAgent` or `TechnicalSupportAgent`). The `result.last_agent.name` will show which agent ultimately handled the query.

*Note: The effectiveness of the handoff depends heavily on the clarity of the `TriageAgent`'s instructions and the LLM's ability to correctly interpret the user's intent and map it to the appropriate specialist. You might need to refine instructions or provide examples to the LLM for better performance.* The `Handoff` primitive is implicitly handled by the SDK when the LLM decides to delegate to another agent it knows about.

---

## Key Takeaways

*   **Handoffs** are implemented by defining specialized agents and instructing an orchestrator agent to delegate tasks.
*   The OpenAI Agents SDK facilitates the seamless transfer of control and context between agents when a handoff is initiated by the LLM.
*   Clear and precise instructions for your orchestrator agent are vital for accurate handoff decisions.
*   Implementing handoffs allows you to build modular, scalable, and highly specialized multi-agent systems.

Today, you've taken a significant step in building truly collaborative AI systems. Tomorrow, we'll continue our journey into multi-agent orchestration by exploring more advanced patterns for managing complex workflows where multiple agents collaborate.
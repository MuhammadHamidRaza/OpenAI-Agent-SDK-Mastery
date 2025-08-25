# Day 13: Intro to `Handoffs`

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 13 of the **OpenAI Agent SDK Mastery** course! Yesterday, we explored the compelling reasons behind building Multi-Agent Systems, where specialized agents collaborate to solve complex problems. Today, we introduce the core mechanism that enables this collaboration: **Handoffs**. A handoff is the process by which one agent delegates a task or transfers control and context to another agent, typically a specialist better equipped to handle a particular sub-problem. Understanding handoffs is fundamental to designing robust and efficient multi-agent workflows, allowing you to build systems that mimic real-world team dynamics.

---

### **TL;DR**

*   **Handoffs:** Structured transfer of responsibility and context from one agent to another.
*   Enable **specialization**, **modularity**, **scalability**, and **robustness** in multi-agent systems.
*   The SDK facilitates handoffs, allowing agents to delegate tasks seamlessly.

---

### **Objectives**

*   Understand the concept and importance of handoffs in multi-agent systems.
*   Learn how handoffs enable specialization and collaboration between agents.
*   Explore the conceptual flow of a handoff within the Agent SDK.
*   Implement basic and advanced handoff scenarios with code examples.

---

## 1) What is a Handoff?

In the context of AI agents, a **handoff** is a structured transfer of responsibility and relevant information from one agent (the *source* agent) to another agent (the *target* agent). It's akin to a manager delegating a task to an expert on their team, providing all the necessary context for the expert to succeed.

### Key Characteristics of a Handoff:

*   **Delegation of Responsibility:** The source agent recognizes that a part of the task falls outside its expertise or is better handled by another agent.
*   **Context Transfer:** Crucial information, such as the user's original query, previous conversation turns, or intermediate results, is passed along to the target agent.
*   **Specialization:** Handoffs are typically used to leverage the specialized knowledge, instructions, or tools of the target agent.
*   **Seamless Transition:** Ideally, the transition should be smooth, allowing the overall system to continue working towards the user's goal without interruption.

---

## 2) Why are Handoffs Important in Multi-Agent Systems?

Handoffs are the glue that holds multi-agent systems together, providing several critical benefits:

1.  **Leveraging Specialization:** Ensures that each part of a complex task is handled by the agent best suited for it. This leads to more accurate, efficient, and high-quality outcomes.
2.  **Modularity and Simplicity:** Each agent can remain focused on its core competency, reducing the complexity of individual agents. Instead of one monolithic agent trying to do everything, you have a network of simpler, specialized agents.
3.  **Improved Scalability:** Different specialized agents can be developed, deployed, and scaled independently, allowing for more flexible system growth.
4.  **Enhanced Robustness:** If one agent fails or struggles with a task, the overall system can potentially recover or re-route the task to another agent, improving overall system resilience.
5.  **Clearer Debugging and Observability:** By explicitly defining handoff points, it becomes easier to trace the flow of a task through the system and identify which agent is responsible for which part of the process.
6.  **Mimicking Real-World Workflows:** Handoffs naturally align with how human teams collaborate, making the design and understanding of multi-agent systems more intuitive.

---

## 3) How Handoffs Work (Conceptual Flow)

While the exact implementation details will vary by SDK, the conceptual flow of a handoff typically involves these steps:

1.  **Initial Prompt:** A user sends a query or task to the primary (or orchestrator) agent.
2.  **Source Agent Processing:** The source agent analyzes the prompt. Based on its instructions and the nature of the query, it determines if a handoff is necessary.
3.  **Handoff Decision:** The source agent identifies the appropriate target agent for the sub-task. This decision is often driven by the LLM's ability to recognize the need for a specialist.
4.  **Handoff Call Generation:** The LLM of the source agent generates a structured "handoff call," specifying the target agent and any context or parameters to be passed.
5.  **SDK Interception:** The OpenAI Agents SDK (or your custom orchestration logic) intercepts this handoff call.
6.  **Context Transfer:** The SDK ensures that the necessary conversational history and any specific data are transferred to the target agent.
7.  **Target Agent Activation:** The target agent is activated with the new context and begins processing the sub-task.
8.  **Target Agent Completion:** The target agent completes its task, potentially returning a result to the source agent or directly to the user/orchestrator.

### Analogy: The Medical Clinic

Think of a medical clinic:

*   **Receptionist (Orchestrator Agent):** Greets the patient (user query) and determines the general nature of their visit.
*   **General Practitioner (Source Agent):** Examines the patient. If the issue is simple (e.g., common cold), they handle it. If it's complex (e.g., heart problem), they recognize the need for a specialist.
*   **Handoff:** The GP refers the patient (and their medical history/symptoms) to a cardiologist.
*   **Cardiologist (Target Agent):** Receives the patient and their context, then uses their specialized knowledge and tools (e.g., ECG machine) to diagnose and treat the heart problem.
*   **Result:** The cardiologist provides a diagnosis and treatment plan, which might be communicated back to the GP or directly to the patient.

---

## 4) Code Examples

This section provides practical examples of implementing handoffs.

### Example 1: Simple Handoff System (`simple_handoff.py`)

This system has two agents: a general assistant that hands off math questions to a math expert.

```python
from agents import Agent, Runner
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY in the .env file.")
    exit()

# Define the General Agent
general_agent = Agent(
    name="HelperBuddy",
    instructions="You’re a friendly assistant who answers general questions. For math questions, hand off to MathBuddy."
)

# Define the Math Agent
math_agent = Agent(
    name="MathBuddy",
    instructions="You’re a math expert who answers math questions in short replies."
)

# Create a Runner
runner = Runner()

# Ask a general question
result1 = runner.run_sync(
    general_agent,
    "What’s a fish?"
)
print("General Answer:", result1.final_output)

# Ask a math question (handoff to MathBuddy)
result2 = runner.run_sync(
    general_agent,
    "What is 6 plus 9?"
)
print("Math Answer:", result2.final_output)
```

### Example 2: Advanced Handoff System (`advanced_handoff.py`)

This system combines handoffs, a math tool, a session for memory, and tracing.

```python
import asyncio
from agents import Agent, Runner, Session, function_tool
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY in the .env file.")
    exit()

# Define a math tool
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

# Define the General Agent
general_agent = Agent(
    name="HelperBuddy",
    instructions="You’re a friendly assistant who answers general questions. For math questions, hand off to MathBuddy."
)

# Define the Math Agent with a tool
math_agent = Agent(
    name="MathBuddy",
    instructions="You’re a math expert who uses tools to answer math questions.",
    tools=[add_numbers]
)

# Create a Session
session = Session()

async def main():
    runner = Runner()
    # Ask a general question with tracing
    print("General Question:")
    result1 = await runner.run(
        general_agent,
        "What’s a bird?",
        session=session
    )
    print("Answer:", result1.final_output)
    # print("Messages:", result1.messages) # Uncomment for full messages
    # print("Status:", result1.status)     # Uncomment for status

    # Ask a math question (handoff to MathBuddy with tool)
    print("\nMath Question:")
    result2 = await runner.run(
        general_agent,
        "What’s 7 plus 3?",
        session=session
    )
    print("Answer:", result2.final_output)

    # Ask a follow-up question
    print("\nFollow-Up Question:")
    result3 = await runner.run(
        general_agent,
        "Can they fly?",
        session=session
    )
    print("Answer:", result3.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 3: Support Handoff System (Conceptual)

This conceptual example shows how a support agent might hand off to a billing agent.

```python
from agents import Agent, Runner

# Define agents
support_agent = Agent(
    name="SupportAgent",
    instructions="Handle customer FAQs about products."
)

billing_agent = Agent(
    name="BillingAgent",
    instructions="Handle all billing, invoices, and payment-related queries."
)

# Runner with multiple agents
runner = Runner(agents=[support_agent, billing_agent])

async def main():
    # Start with support agent
    result = await runner.run(support_agent, "I have a problem with my last invoice.")
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

---

## 5) Key Takeaways

*   **Handoffs** are the fundamental mechanism for task delegation and collaboration in Multi-Agent Systems.
*   They enable agents to leverage **specialization**, leading to more efficient, modular, and robust AI applications.
*   Handoffs involve the structured transfer of responsibility and context from a source agent to a target agent.
*   The OpenAI Agents SDK provides built-in support for facilitating these handoffs, simplifying the orchestration of complex agent workflows.

---

Today, you've grasped the theoretical importance of handoffs and seen practical examples of their implementation. Tomorrow, we'll continue our journey into multi-agent systems by introducing **Guardrails**, another critical primitive for ensuring the safety and reliability of your agentic applications.
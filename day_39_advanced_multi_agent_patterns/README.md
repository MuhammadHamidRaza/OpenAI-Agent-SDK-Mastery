# Day 39: Advanced Multi-Agent Patterns

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 39 of the **OpenAI Agent SDK Mastery** course! You've built multi-agent systems with basic handoffs and sequential workflows. Today, we delve into **Advanced Multi-Agent Patterns**, exploring more sophisticated collaboration models that enable agents to tackle highly complex, dynamic, and even uncertain problems. We'll examine patterns like hierarchical multi-agent systems (supervisor/worker), blackboard architectures, and the crucial concept of human-in-the-loop integration. By the end of this session, you'll be equipped to design and implement robust, scalable, and adaptable agent teams that can operate effectively in challenging real-world scenarios.

---

## Beyond Simple Handoffs: The Need for Advanced Patterns

While sequential and simple parallel orchestrations are effective for many tasks, some problems demand more dynamic and flexible collaboration:

*   **Dynamic Task Allocation:** When sub-tasks are not known upfront or change based on intermediate results.
*   **Complex Decision-Making:** Requiring consensus or iterative refinement among multiple experts.
*   **Uncertainty and Ambiguity:** When agents need to share information and collectively resolve ambiguities.
*   **Human Oversight and Intervention:** Integrating human expertise and judgment into automated workflows.

Advanced multi-agent patterns provide frameworks to address these complexities.

---

## Key Advanced Multi-Agent Patterns

### 1. Hierarchical Multi-Agent Systems (Supervisor/Worker)

*   **Concept:** A top-down structure where a high-level "supervisor" agent breaks down complex problems, delegates sub-tasks to lower-level "worker" agents, and then synthesizes their results. Worker agents focus on specific, well-defined tasks.
*   **Benefits:** Clear division of labor, improved scalability, easier management of complexity, supervisor can handle overall strategy and error recovery.
*   **Analogy:** A project manager (supervisor) assigning tasks to team members (workers) and overseeing the project's progress.
*   **Example Use Case:** A research manager agent overseeing web search, data analysis, and report writing agents.

### 2. Blackboard Architecture

*   **Concept:** A shared global workspace (the "blackboard") where agents (knowledge sources) can read and write information. Agents operate asynchronously, reacting to changes on the blackboard and contributing their expertise when relevant.
*   **Benefits:** Highly flexible, supports opportunistic problem-solving, good for problems where the solution path is not predefined, easy to add/remove agents.
*   **Analogy:** A shared whiteboard in a team meeting where everyone contributes ideas and solutions as they come to mind.
*   **Example Use Case:** Complex diagnostic systems, design automation, multi-modal data fusion.

### 3. Human-in-the-Loop (HITL)

*   **Concept:** Explicitly integrates human judgment and intervention into the agent workflow. The agent performs tasks autonomously until it encounters a situation where human expertise is required (e.g., ambiguity, ethical dilemma, high-stakes decision, or when confidence is low).
*   **Benefits:** Combines the efficiency of AI with the nuanced reasoning and ethical judgment of humans, improves trust, enables continuous learning for the AI.
*   **Analogy:** An automated customer service system escalating complex queries to a human agent.
*   **Example Use Case:** Content moderation, medical diagnosis, legal review, complex customer support.

---

## Implementing Advanced Patterns (Conceptual)

Implementing these patterns often involves careful design of agent instructions, communication protocols, and the use of SDK primitives like handoffs and tools.

### Example: Conceptual Human-in-the-Loop Workflow

Let's outline a scenario where an agent seeks human approval for a sensitive action.

```python
from agents import Agent, Runner
import os

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define a sensitive action agent
sensitive_action_agent = Agent(
    name="SensitiveActionAgent",
    instructions=(
        "You are an agent responsible for performing sensitive actions. "
        "Before executing any action that requires human approval, you must clearly state the action and ask for confirmation. "
        "Wait for explicit human confirmation before proceeding. "
        "If confirmed, proceed; otherwise, state that the action was cancelled." 
    )
)

def get_human_confirmation(prompt: str) -> bool:
    """Simulates getting human confirmation."""
    print(f"\n[HUMAN INTERVENTION REQUIRED]: {prompt}")
    response = input("Type 'yes' to confirm, 'no' to cancel: ").lower().strip()
    return response == 'yes'

# Orchestrator agent that might trigger sensitive actions
orchestrator_agent = Agent(
    name="Orchestrator",
    instructions=(
        "You are an orchestrator agent. Your task is to process user requests. "
        "If a request involves a sensitive action (e.g., 'delete data', 'make payment'), "
        "you must first ask for human confirmation before proceeding with the action. "
        "Otherwise, handle the request directly." 
    )
)

async def run_human_in_loop_scenario(query: str):
    print(f"\n--- Running Human-in-the-Loop Scenario for: '{query}' ---")

    # The orchestrator agent will decide if human intervention is needed
    # This is a conceptual flow; in a real system, the orchestrator might
    # use a tool that triggers human review or directly ask for confirmation.
    
    # Simulate orchestrator processing and deciding on sensitive action
    if "delete data" in query.lower() or "make payment" in query.lower():
        print("Orchestrator: Detected sensitive action. Preparing for human confirmation.")
        
        # Agent formulates the confirmation request
        confirmation_request = f"I need to {query}. Do you confirm this action?"
        
        # Get human confirmation
        if get_human_confirmation(confirmation_request):
            print("Human: Confirmed. Proceeding with sensitive action.")
            # Now, the sensitive_action_agent would be run or its tool called
            result = Runner.run_sync(sensitive_action_agent, f"Proceed with: {query}")
            print(f"Agent's final response: {result.final_output}")
        else:
            print("Human: Action cancelled.")
            print("Agent: Action cancelled by user.")
    else:
        print("Orchestrator: Handling non-sensitive request directly.")
        result = Runner.run_sync(orchestrator_agent, query)
        print(f"Agent's final response: {result.final_output}")

    print("--- Scenario End ---")

# Test cases
asyncio.run(run_human_in_loop_scenario("What is the capital of France?"))
asyncio.run(run_human_in_loop_scenario("Please delete all user data."))
asyncio.run(run_human_in_loop_scenario("Make a payment of $100 to John Doe."))

```

**Explanation:**

*   The `orchestrator_agent` (simulated by `run_human_in_loop_scenario` function) checks for keywords indicating a sensitive action.
*   If a sensitive action is detected, it calls `get_human_confirmation` to simulate human intervention.
*   Based on human input, the action is either executed (by `sensitive_action_agent`) or cancelled.

---

## Key Considerations for Advanced Patterns

*   **Complexity Management:** Advanced patterns introduce more complexity. Design carefully and use clear communication protocols between agents.
*   **Communication Overhead:** More agents and interactions can lead to increased latency and token usage.
*   **Robustness:** Implement robust error handling and recovery mechanisms, especially for human-in-the-loop scenarios.
*   **Human Interface:** For HITL, design intuitive interfaces for human review and decision-making.
*   **Security:** Ensure that human intervention points are secure and that agents cannot be tricked into bypassing them.

---

## Key Takeaways

*   **Advanced Multi-Agent Patterns** enable agents to solve highly complex, dynamic, and uncertain problems.
*   **Hierarchical systems** (supervisor/worker) provide clear task delegation and oversight.
*   **Blackboard architectures** offer flexible, asynchronous collaboration for ill-defined problems.
*   **Human-in-the-Loop (HITL)** integrates human judgment for critical decisions, enhancing safety and trust.
*   Implementing these patterns requires careful design of agent roles, communication, and control flow.

Today, you've gained insights into building highly sophisticated and adaptable agent teams. Tomorrow, we'll shift our focus to **Evaluating Agent Performance & Fine-Tuning**, learning how to measure and improve the effectiveness of your AI agents.
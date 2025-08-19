# Day 19: Orchestrating Multi-Agent Workflows

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 19 of the **OpenAI Agent SDK Mastery** course! You've learned how to implement basic handoffs, allowing one agent to delegate a task to another. Today, we expand on this by diving into **Orchestrating Multi-Agent Workflows**. This involves designing and managing complex interactions where multiple agents collaborate in structured ways to achieve a larger, more intricate goal. We'll explore various orchestration patterns—sequential, parallel, and hierarchical—and discuss how to effectively manage the flow of information and control across your agent team. By the end of this session, you'll be equipped to design sophisticated multi-agent systems that can tackle real-world problems requiring diverse expertise and coordinated effort.

---

## Beyond Simple Handoffs: The Need for Orchestration

While a direct handoff is powerful, many complex tasks require more than a simple one-to-one delegation. Consider scenarios where:

*   A task needs to go through a specific sequence of steps, each handled by a different specialist.
*   Multiple sub-tasks can be performed simultaneously.
*   A high-level agent needs to oversee and coordinate the work of several sub-agents.
*   Results from one agent's work are inputs for another.

**Orchestration** is the art and science of coordinating these interactions, ensuring that agents work together efficiently and effectively towards a common objective. It defines the overall architecture and communication protocols for your agent team.

---

## Common Multi-Agent Orchestration Patterns

### 1. Sequential Orchestration (Pipeline)

*   **Description:** Tasks are processed in a linear fashion, where the output of one agent becomes the input for the next. This is the most straightforward form of orchestration.
*   **Analogy:** An assembly line, where each station (agent) performs a specific step before passing the product to the next station.
*   **Use Cases:** Data processing pipelines (e.g., extract -> transform -> load), content generation workflows (e.g., research -> draft -> edit -> publish), multi-step problem-solving.
*   **Example Flow:**
    1.  `ResearchAgent` finds information.
    2.  `AnalysisAgent` analyzes the information from `ResearchAgent`.
    3.  `SummarizerAgent` summarizes the analysis from `AnalysisAgent`.

### 2. Parallel Orchestration

*   **Description:** Multiple agents work on different sub-tasks simultaneously. Their results are then combined or synthesized by a coordinating agent.
*   **Analogy:** A team of researchers simultaneously investigating different aspects of a problem, then presenting their findings to a lead researcher.
*   **Use Cases:** Gathering information from multiple sources, performing independent calculations, generating diverse creative outputs, A/B testing different approaches.
*   **Example Flow:**
    1.  `QueryAgent` receives a request.
    2.  `WebSearchAgent` and `DatabaseSearchAgent` simultaneously search for information.
    3.  `SynthesisAgent` combines results from both search agents.

### 3. Hierarchical Orchestration (Supervisor/Sub-Agent)

*   **Description:** A high-level "supervisor" or "manager" agent oversees and delegates tasks to lower-level "worker" or "sub-agents." The supervisor agent is responsible for breaking down complex problems, assigning tasks, and integrating results.
*   **Analogy:** A project manager delegating tasks to team members and then reviewing their work.
*   **Use Cases:** Complex project management, recursive problem-solving, managing large-scale agent systems, dynamic task allocation.
*   **Example Flow:**
    1.  `ProjectManagerAgent` receives a complex project.
    2.  `ProjectManagerAgent` breaks it into sub-tasks and assigns them to `CodeAgent`, `TestAgent`, `DocAgent`.
    3.  Sub-agents complete their tasks and report back to `ProjectManagerAgent`.
    4.  `ProjectManagerAgent` integrates results and provides final output.

---

## Managing Flow and Context in Orchestrated Workflows

Effective orchestration requires careful management of:

*   **Information Flow:** Ensuring that the right data and context are passed between agents at each step. This often involves passing `RunResult` objects or specific data extracted from them.
*   **Control Flow:** Defining the sequence of agent activations. This can be explicit (e.g., `if-else` logic, state machines) or implicit (e.g., LLM-driven handoffs).
*   **Error Handling:** Implementing mechanisms to gracefully handle failures in individual agents or tools, and potentially re-routing tasks.

### Conceptual Example: Sequential Workflow

Let's outline a conceptual sequential workflow for generating a short report based on a user query.

```python
from agents import Agent, Runner
from agents.tools import WebSearchTool, function_tool
import os

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Assume WebSearchTool is configured
web_search_tool = WebSearchTool()

@function_tool
def analyze_text(text: str) -> str:
    """Analyzes a given text and extracts key insights or themes."""
    # In a real scenario, this would involve more sophisticated NLP or LLM calls
    return f"Analysis of text: Key points identified. Text length: {len(text)} characters."

@function_tool
def summarize_text(text: str) -> str:
    """Summarizes a given text concisely."""
    # In a real scenario, this would involve more sophisticated summarization
    return f"Summary: {text[:100]}... (truncated)"

# Define specialized agents
research_agent = Agent(
    name="ResearchAgent",
    instructions="You are a research assistant. Use web search to find information relevant to the user's query.",
    tools=[web_search_tool]
)

analysis_agent = Agent(
    name="AnalysisAgent",
    instructions="You are an analysis expert. Analyze the provided research findings and extract key insights.",
    tools=[analyze_text]
)

summarizer_agent = Agent(
    name="SummarizerAgent",
    instructions="You are a summarization expert. Summarize the provided analysis into a concise report.",
    tools=[summarize_text]
)

# Orchestrator function to manage the workflow
def run_report_workflow(query: str):
    print(f"\n--- Starting Report Generation Workflow for: '{query}' ---")

    # Step 1: Research
    print("Step 1: Researching...")
    research_result = Runner.run_sync(research_agent, query)
    research_findings = research_result.final_output
    print(f"Research Findings: {research_findings[:200]}...")

    # Step 2: Analysis (pass research findings as input)
    print("\nStep 2: Analyzing research findings...")
    analysis_result = Runner.run_sync(analysis_agent, research_findings)
    analysis_output = analysis_result.final_output
    print(f"Analysis Output: {analysis_output[:200]}...")

    # Step 3: Summarization (pass analysis output as input)
    print("\nStep 3: Summarizing analysis...")
    summary_result = Runner.run_sync(summarizer_agent, analysis_output)
    final_report = summary_result.final_output
    print(f"Final Report: {final_report}")

    print("\n--- Workflow Completed ---")
    return final_report

# Run the workflow
run_report_workflow("Recent advancements in quantum computing")

```

**Explanation:**

*   We define three specialized agents: `ResearchAgent`, `AnalysisAgent`, and `SummarizerAgent`.
*   The `run_report_workflow` function acts as the orchestrator. It explicitly calls each agent in sequence, passing the `final_output` of one agent as the input to the next.
*   This demonstrates a simple sequential pipeline. More complex orchestrations would involve conditional logic, loops, or more sophisticated control flow mechanisms.

---

## Key Takeaways

*   **Orchestration** is essential for coordinating multiple agents to solve complex problems.
*   Common patterns include **sequential**, **parallel**, and **hierarchical** workflows.
*   Effective orchestration requires careful management of **information flow** (passing data between agents) and **control flow** (defining the sequence of agent activations).
*   The OpenAI Agents SDK provides the building blocks (agents, tools, handoffs) that you can combine with standard Python logic to implement these orchestration patterns.

Today, you've gained a deeper understanding of how to design and manage complex multi-agent systems. Tomorrow, we'll explore **Agent Planning**, where agents can autonomously plan a sequence of actions to solve a problem, adding another layer of intelligence to your agentic applications.
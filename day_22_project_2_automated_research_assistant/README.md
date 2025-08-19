# Day 22: Project 2: Automated Research Assistant

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 22 of the **OpenAI Agent SDK Mastery** course! You've now mastered individual agent capabilities, tool integration, memory management, and even advanced patterns like ReAct. Today, we bring these concepts together in your second major project: building an **Automated Research Assistant**. This project will demonstrate the power of multi-agent systems by creating a team of specialized agents that collaborate to find information, analyze it, and generate a comprehensive report on a given topic. You'll apply your knowledge of agent definition, tool usage (especially web search), and orchestration to build a truly intelligent research system.

---

## Project Goal: Automated Research Assistant

Your goal is to build a system that can take a research query from a user, autonomously gather information from the web, process and synthesize that information, and then present a well-structured report. This will involve:

1.  **Receiving a Research Query:** The initial input from the user.
2.  **Information Gathering:** Using a web search tool to find relevant articles, data, and facts.
3.  **Information Analysis/Synthesis:** Processing the raw search results to extract key insights and eliminate redundancy.
4.  **Report Generation:** Compiling the synthesized information into a coherent and readable report.

### Multi-Agent Approach:

We will use a multi-agent approach, where each agent specializes in a particular phase of the research process:

*   **`OrchestratorAgent` (or `ResearchManager`):** Receives the initial query, breaks it down, and delegates tasks to other agents. It also compiles the final report.
*   **`WebResearcherAgent`:** Specializes in using the `WebSearchTool` to find information based on specific sub-queries.
*   **`AnalystAgent`:** Specializes in processing raw text, extracting key points, and synthesizing information from the `WebResearcherAgent`'s findings.
*   **`ReportWriterAgent`:** Specializes in structuring and formatting the analyzed information into a final report.

---

## Step-by-Step Implementation

### Step 1: Setup and Tool Definition

Ensure your environment is configured with your OpenAI API key and any necessary API keys for the `WebSearchTool`.

```python
import os
from agents import Agent, Runner
from agents.tools import WebSearchTool, function_tool

# --- Configuration --- #
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()

# Initialize the WebSearchTool (requires proper API key setup for a real search service)
web_search_tool = WebSearchTool()

# Define a simple analysis tool (conceptual for this example)
@function_tool
def analyze_text_for_research(text: str) -> str:
    """Analyzes a block of research text to extract key facts and insights.
    This function simulates a more complex analysis by an LLM.
    """
    # In a real scenario, this would involve another LLM call or more sophisticated NLP
    if len(text) > 500:
        return f"Analyzed a large document. Key insights extracted from first 500 chars: {text[:500]}..."
    return f"Analyzed: {text}. Key points identified."

print("Setup complete and tools initialized.")
```

### Step 2: Define Specialized Agents

Create the `WebResearcherAgent`, `AnalystAgent`, and `ReportWriterAgent`.

```python
# ... (previous code for imports and setup) ...

web_researcher_agent = Agent(
    name="WebResearcherAgent",
    instructions="You are an expert web researcher. Use the WebSearchTool to find comprehensive and relevant information for a given query. Provide the raw search results.",
    tools=[web_search_tool]
)

analyst_agent = Agent(
    name="AnalystAgent",
    instructions="You are a skilled information analyst. Your task is to synthesize raw research findings, extract key facts, and identify important themes. Provide a concise summary of your analysis.",
    tools=[analyze_text_for_research]
)

report_writer_agent = Agent(
    name="ReportWriterAgent",
    instructions="You are a professional report writer. Your task is to take analyzed information and format it into a well-structured, clear, and concise research report. Include an introduction, key findings, and a conclusion."
)

print("Specialized agents defined.")
```

### Step 3: Implement the `OrchestratorAgent` (Research Manager)

This agent will manage the overall workflow, delegating tasks and compiling the final report.

```python
# ... (previous code for imports, setup, and specialized agents) ...

class ResearchManager:
    def __init__(self, researcher, analyst, writer):
        self.researcher = researcher
        self.analyst = analyst
        self.writer = writer

    def conduct_research(self, query: str) -> str:
        print(f"\n--- Research Manager: Starting research for '{query}' ---")

        # Step 1: Web Research
        print("Research Manager: Delegating to WebResearcherAgent...")
        research_result = Runner.run_sync(self.researcher, f"Find comprehensive information about: {query}")
        raw_findings = research_result.final_output
        print(f"Research Manager: Received raw findings (truncated): {raw_findings[:200]}...")

        # Step 2: Analysis
        print("\nResearch Manager: Delegating to AnalystAgent for analysis...")
        analysis_result = Runner.run_sync(self.analyst, raw_findings)
        analyzed_info = analysis_result.final_output
        print(f"Research Manager: Received analyzed info (truncated): {analyzed_info[:200]}...")

        # Step 3: Report Writing
        print("\nResearch Manager: Delegating to ReportWriterAgent for report generation...")
        report_result = Runner.run_sync(self.writer, analyzed_info)
        final_report = report_result.final_output
        print("Research Manager: Final report generated.")

        print("\n--- Research Manager: Research complete ---")
        return final_report

# Instantiate the manager
research_manager = ResearchManager(
    researcher=web_researcher_agent,
    analyst=analyst_agent,
    writer=report_writer_agent
)

print("Research Manager instantiated.")
```

### Step 4: Run the Automated Research Assistant

Now, let's put it all together and run the research assistant with a query.

```python
# ... (previous code for imports, setup, specialized agents, and ResearchManager class) ...

# Example Research Query
research_query = "The impact of artificial intelligence on the future of work."

# Conduct the research
final_research_report = research_manager.conduct_research(research_query)

print("\n--- FINAL RESEARCH REPORT ---")
print(final_research_report)
print("---------------------------")

```

---

## Key Takeaways from Project 2

*   You've successfully built a **multi-agent research system**, demonstrating how specialized agents can collaborate in a structured workflow.
*   The `ResearchManager` acts as an orchestrator, delegating tasks sequentially to `WebResearcherAgent`, `AnalystAgent`, and `ReportWriterAgent`.
*   This project highlights the power of **modularity** and **specialization** in complex AI tasks.
*   You've applied your knowledge of agent definition, tool integration (especially `WebSearchTool`), and basic orchestration patterns.

Congratulations on completing your second major project! This project showcases the practical application of multi-agent systems. Tomorrow, we'll delve into **Agent Reflection & Self-Correction**, enabling your agents to evaluate their own work and improve their performance.
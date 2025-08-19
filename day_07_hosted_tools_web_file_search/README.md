# Day 7: Hosted Tools: Web & File Search

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 7 of the **OpenAI Agent SDK Mastery** course! Over the past few days, you've learned how to define and integrate your own custom Python functions as tools for your agents. Today, we'll explore another powerful aspect of the SDK: **hosted or built-in tools**. These are pre-packaged tools that provide immediate access to common functionalities like web search and file system interaction. By leveraging these tools, your agents can tap into vast amounts of real-time information and interact with local files, significantly expanding their utility and intelligence without requiring you to write complex integrations from scratch.

---

## The Power of Built-in Tools

While custom tools allow for highly specific functionalities, built-in tools offer immediate access to common, powerful capabilities. The OpenAI Agents SDK provides several such tools that are ready to be used with minimal setup. These tools are designed to address frequent needs of agents, such as:

*   **Accessing Real-time Information:** The internet is a dynamic source of information. A web search tool allows agents to query this information, overcoming the LLM's knowledge cut-off.
*   **Interacting with Local Data:** Agents might need to read from or write to files on the local system to process data, store results, or retrieve context.

Using built-in tools is similar to using your custom tools; you simply include them in the `tools` list when defining your agent.

---

## `WebSearchTool`: Giving Your Agent Access to the Internet

One of the most powerful built-in tools is the `WebSearchTool`. This tool enables your agent to perform web searches and retrieve information from the internet. This is crucial for tasks requiring up-to-date data, current events, or information not present in the LLM's training data.

To use `WebSearchTool`, you typically need to provide an API key for a search service (like Google Search API). The SDK integrates with these services to perform the actual search.

### Example: Agent Performing a Web Search

```python
from agents import Agent, Runner
from agents.tools import WebSearchTool # Assuming WebSearchTool is available here
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

# For WebSearchTool, you might need a separate API key, e.g., for Google Custom Search Engine
# os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY" 
# os.environ["GOOGLE_CSE_ID"] = "YOUR_GOOGLE_CSE_ID" # If using Google Custom Search

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Initialize the WebSearchTool
# The exact initialization might vary based on SDK version and search backend
web_search_tool = WebSearchTool()

# Define an agent and provide the WebSearchTool
research_agent = Agent(
    name="ResearchAgent",
    instructions="You are a helpful research assistant. Use web search to find up-to-date information.",
    tools=[web_search_tool]
)

# Run the agent with a query that requires web search
print("Running ResearchAgent with web search...")
result = Runner.run_sync(research_agent, "What is the current population of Tokyo?")

# Print the final output
print("Agent's response:", result.final_output)

# Another example
print("\nRunning ResearchAgent for recent news...")
result2 = Runner.run_sync(research_agent, "Summarize the latest news about AI advancements.")
print("Agent's response:", result2.final_output)

```

*Note: The exact import path and initialization of `WebSearchTool` might vary based on the specific version and configuration of the OpenAI Agents SDK. You may need to consult the official SDK documentation for the most accurate usage.* For this example, we assume `WebSearchTool` is directly importable from `agents.tools`.

---

## `FileSearchTool` (Conceptual): Interacting with the File System

While `WebSearchTool` handles external information, an agent might also need to interact with local files. A `FileSearchTool` (or similar file system tools) would allow agents to:

*   **Read Files:** Access content from local documents, configuration files, or data files.
*   **Write Files:** Save generated reports, logs, or processed data.
*   **List Directories:** Understand the structure of local folders.

### Example: Agent Interacting with Files (Conceptual)

```python
from agents import Agent, Runner
# from agents.tools import FileSearchTool # Assuming FileSearchTool is available
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Conceptual FileSearchTool initialization
# file_search_tool = FileSearchTool()

# Define an agent that can use file tools
file_agent = Agent(
    name="FileAgent",
    instructions="You can read and write files on the local system.",
    # tools=[file_search_tool] # Add file tool here if available
)

# Conceptual run: Agent asked to read a file
# print("Running FileAgent to read a file...")
# result = Runner.run_sync(file_agent, "Read the content of 'report.txt'.")
# print("Agent's response:", result.final_output)

print("File interaction tools are powerful for local data processing.")
print("Please refer to the official SDK documentation for specific built-in file system tools and their usage.")

```

*Note: The OpenAI Agents SDK might provide specific tools for file system operations (e.g., `read_file`, `write_file`, `list_directory`). The `FileSearchTool` is used here as a conceptual placeholder. Always refer to the latest SDK documentation for the exact names and functionalities of built-in file system tools.* The `default_api` in the current environment provides `read_file`, `write_file`, `list_directory`, and `search_file_content` which are analogous to what a `FileSearchTool` might encapsulate.

---

## Key Takeaways

*   Built-in or hosted tools significantly extend an agent's capabilities without custom development.
*   `WebSearchTool` is essential for giving agents access to real-time and up-to-date information from the internet.
*   Tools for file system interaction (like conceptual `FileSearchTool` or specific `read_file`/`write_file` functions) enable agents to process and manage local data.
*   Always consult the official SDK documentation for the most accurate and up-to-date information on built-in tools and their required configurations (e.g., API keys).

By integrating these powerful hosted tools, your agents become even more versatile and capable of handling a wider range of real-world tasks. Tomorrow, we'll shift our focus to **Agent Memory**, understanding how agents can remember past interactions and maintain conversational context.
# Day 44: Project 5: Ultimate Personal Assistant

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 44 of the **OpenAI Agent SDK Mastery** course! This is it—your final and most ambitious project. Over the past 43 days, you've built a robust foundation in AI agents, mastering concepts from basic execution and tool integration to advanced topics like multi-agent systems, real-time processing, and long-term memory. Today, you will synthesize all this knowledge to build the **Ultimate Personal Assistant**. This project aims to create an all-in-one intelligent agent that integrates voice interaction, real-time data analysis, and a sophisticated multi-agent architecture to handle a wide range of personal and professional tasks. Get ready to apply everything you've learned to build a truly comprehensive and powerful AI companion.

---

## Project Goal: The Ultimate Personal Assistant

Your goal is to design and conceptually implement a personal assistant that can:

1.  **Understand and respond to voice commands** (using STT/TTS).
2.  **Manage tasks and calendar entries** (persistent memory).
3.  **Provide real-time information** (e.g., weather, stock prices, news).
4.  **Answer general knowledge questions** (web search/RAG).
5.  **Perform complex, multi-step operations** through multi-agent collaboration.
6.  **Maintain context** across interactions.

### Architectural Vision:

This project will likely involve a hierarchical multi-agent system, with a central `OrchestratorAgent` delegating tasks to specialized sub-agents. Each sub-agent will have its own set of tools and potentially its own memory. The entire system will be wrapped in a voice interface.

*   **`VoiceInterface`:** Handles STT and TTS, acting as the primary user interface.
*   **`OrchestratorAgent`:** The central brain, routing requests to appropriate specialized agents.
*   **`TaskManagementAgent`:** Manages tasks and calendar (using custom tools and persistent memory).
*   **`InformationRetrievalAgent`:** Handles web search and RAG for general knowledge.
*   **`RealtimeDataAgent`:** Fetches and analyzes real-time data (e.g., stock, weather).
*   **`GeneralConversationAgent`:** Handles casual chat and non-specific queries.

---

## Step-by-Step Conceptual Implementation

Due to the complexity and scope, this project will be outlined conceptually, demonstrating how the various components you've learned about would fit together. Actual implementation would involve significant coding for each module.

### Step 1: Core Setup and Voice Interface

This involves setting up your environment and integrating conceptual (or actual) STT/TTS services.

```python
import asyncio
import os
from agents import Agent, Runner
from agents.tools import function_tool, WebSearchTool # Assuming WebSearchTool is configured
# from agents import SQLiteSession # For persistent memory

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()

# ---
# Conceptual STT/TTS (from Day 37)
# ---
async def conceptual_stt_service(audio_data) -> str:
    # Simulate STT
    return audio_data # For simplicity, assume text input

async def conceptual_tts_service(text_to_speak: str) -> bytes:
    # Simulate TTS
    return b"simulated_audio_bytes"

async def play_audio(audio_bytes: bytes):
    # Simulate audio playback
    pass

# ---
# Conceptual Tools (from previous days)
# ---
@function_tool
async def add_task_ultimate(description: str, due_date: str = "No due date") -> str:
    """Adds a new task to the ultimate assistant's task list."""
    # In real project, interact with a database or task API
    return f"Task '{description}' added."

@function_tool
async def get_realtime_weather(city: str) -> str:
    """Fetches real-time weather for a city."""
    # In real project, call a weather API
    return f"Weather in {city}: Sunny, 25C."

@function_tool
async def get_stock_quote(ticker: str) -> str:
    """Fetches real-time stock quote for a ticker."""
    # In real project, call a stock API
    return f"Stock {ticker}: $175.20."

# Initialize WebSearchTool (if used)
web_search_tool = WebSearchTool()

print("Core setup and conceptual tools initialized.")
```

### Step 2: Define Specialized Agents

Each agent will have its own instructions and tools.

```python
# ... (previous code for imports, setup, and conceptual tools) ...

task_agent = Agent(
    name="TaskManagementAgent",
    instructions="You manage user tasks and calendar entries. Use task management tools.",
    tools=[add_task_ultimate] # Add other task tools here
)

info_agent = Agent(
    name="InformationRetrievalAgent",
    instructions="You answer general knowledge questions using web search and RAG.",
    tools=[web_search_tool] # Add RAG tool here
)

realtime_agent = Agent(
    name="RealtimeDataAgent",
    instructions="You provide real-time data like weather and stock quotes. Use relevant tools.",
    tools=[get_realtime_weather, get_stock_quote]
)

general_agent = Agent(
    name="GeneralConversationAgent",
    instructions="You are a friendly conversationalist for general chat."
)

print("Specialized agents defined.")
```

### Step 3: Implement the `OrchestratorAgent`

This agent will act as the central router, deciding which specialized agent should handle the user's request. It will use its instructions to determine intent and potentially hand off to other agents.

```python
# ... (previous code for imports, setup, and specialized agents) ...

orchestrator_agent = Agent(
    name="UltimateAssistantOrchestrator",
    instructions=(
        "You are the central orchestrator of the Ultimate Personal Assistant. "
        "Your role is to understand the user's intent and route the request to the most appropriate specialized agent: "
        "- 'TaskManagementAgent' for tasks/calendar. "
        "- 'InformationRetrievalAgent' for general knowledge/web search. "
        "- 'RealtimeDataAgent' for live weather or stock data. "
        "- 'GeneralConversationAgent' for casual chat. "
        "Do not answer questions yourself; only route or hand off. "
    ),
    # The SDK implicitly allows handoffs to other agents defined in the same scope
    # or explicitly passed. The LLM's instructions guide the routing.
)

print("Orchestrator Agent defined.")
```

### Step 4: Create the Main Voice Interaction Loop

This loop will tie everything together, simulating the full voice interaction pipeline.

```python
# ... (previous code for imports, setup, specialized agents, and orchestrator) ...

async def run_ultimate_assistant():
    print("\n--- Ultimate Personal Assistant Ready ---\\n")
    print("Speak your command. Type 'exit' to quit.")

    while True:
        user_spoken_input = input("You (type your voice command): ")
        if user_spoken_input.lower() == 'exit':
            break

        # STT: Convert spoken input to text
        transcribed_text = await conceptual_stt_service(user_spoken_input)
        print(f"[Transcribed]: {transcribed_text}")

        # Orchestrator routes the request
        print("[Orchestrator]: Routing request...")
        # The orchestrator agent will decide which sub-agent to use.
        # The Runner will then execute the chosen sub-agent.
        # We need to pass all potential target agents to the Runner for the orchestrator to choose from.
        # This is a simplified representation; in a real system, you might have a more explicit routing mechanism.
        
        # For this conceptual example, we'll manually route based on keywords for clarity
        # In a real multi-agent system, the orchestrator_agent would make this decision via LLM reasoning.
        target_agent = None
        if "task" in transcribed_text.lower() or "calendar" in transcribed_text.lower():
            target_agent = task_agent
        elif "weather" in transcribed_text.lower() or "stock" in transcribed_text.lower():
            target_agent = realtime_agent
        elif "who is" in transcribed_text.lower() or "what is" in transcribed_text.lower() or "tell me about" in transcribed_text.lower():
            target_agent = info_agent
        else:
            target_agent = general_agent

        print(f"[Orchestrator]: Delegating to {target_agent.name}...")
        
        # Run the selected agent with streaming
        agent_response_text = ""
        print("Assistant: ", end="", flush=True)
        with Runner.run_streamed(target_agent, transcribed_text) as stream:
            async for event in stream:
                if hasattr(event, 'text'):
                    print(event.text, end="", flush=True)
                    agent_response_text += event.text
                elif hasattr(event, 'tool_name'):
                    print(f"\n[Agent using tool: {event.tool_name}]", end="", flush=True)
                elif hasattr(event, 'output'):
                    print(f"\n[Tool output: {event.output}]", end="", flush=True)
            final_result = stream.get_final_result()
            agent_response_text = final_result.final_output # Ensure complete final output
        print("\n")

        # TTS: Convert agent's text response to audio and play
        if agent_response_text:
            synthesized_audio_bytes = await conceptual_tts_service(agent_response_text)
            await play_audio(synthesized_audio_bytes)

    print("Goodbye from your Ultimate Personal Assistant!")

if __name__ == "__main__":
    asyncio.run(run_ultimate_assistant())

```

---

## Key Takeaways from Project 5

*   You've conceptually designed and implemented an **Ultimate Personal Assistant**, integrating a wide array of concepts learned throughout the course.
*   This project demonstrates the power of **hierarchical multi-agent systems**, with an `OrchestratorAgent` routing requests to specialized sub-agents.
*   It combines **voice interaction (STT/TTS)**, **real-time data analysis**, **task management**, and **general knowledge retrieval**.
*   The complexity of such a system highlights the importance of modular design, clear agent instructions, and robust orchestration.

Congratulations on completing your final and most challenging project! You've truly mastered the OpenAI Agent SDK. Tomorrow, we'll conclude our journey with **Final Thoughts & Course Conclusion**, reflecting on your progress and the future of AI agents.
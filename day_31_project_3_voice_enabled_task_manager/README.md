# Day 31: Project 3: Voice-Enabled Task Manager

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 31 of the **OpenAI Agent SDK Mastery** course! You've gained a deep understanding of voice agents, long-term memory, and advanced memory optimization. Today, we bring these powerful concepts together in your third major project: building a **Voice-Enabled Task Manager**. This project will allow you to interact with your task list and calendar using natural spoken commands, demonstrating the seamless integration of speech technologies with intelligent agents and persistent memory. You'll apply your knowledge of STT/TTS (conceptually), agent definition, custom tools for data management, and long-term memory to create a highly interactive and practical application.

---

## Project Goal: Voice-Enabled Task Manager

Your goal is to create an agent that can manage tasks and calendar entries through voice commands. The system should be able to:

1.  **Understand spoken commands** for creating, listing, and completing tasks/events.
2.  **Store and retrieve tasks/events** persistently.
3.  **Respond verbally** with confirmations or requested information.

### Components We'll Use:

*   **Agent:** The core intelligent entity.
*   **Speech-to-Text (STT) & Text-to-Speech (TTS):** For voice input and output (conceptually, using placeholders).
*   **Custom Tools:** For interacting with a task/calendar data store.
*   **Long-Term Memory:** To store tasks/events persistently (e.g., a simple in-memory list or a simulated database).
*   **`Runner`:** To execute the agent.

---

## Step-by-Step Implementation

### Step 1: Setup and Conceptual Voice Integration

We'll simulate STT and TTS for this project, focusing on the agent logic.

```python
import os
from agents import Agent, Runner
from agents.tools import function_tool

# Ensure your OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()

# ---
Conceptual STT and TTS Functions ---
---
def conceptual_stt(audio_input: str) -> str:
    """Simulates Speech-to-Text conversion."""
    print(f"[STT]: Transcribing '{audio_input}'...")
    return audio_input # In a real app, this would be a call to an STT service

def conceptual_tts(text_output: str) -> str:
    """Simulates Text-to-Speech conversion."""
    print(f"[TTS]: Synthesizing '{text_output}'...")
    return f"[Audio: {text_output}]" # In a real app, this would be a call to a TTS service

print("Conceptual STT/TTS functions ready.")
```

### Step 2: Define Custom Tools for Task Management

We'll create tools to add, list, and complete tasks. For simplicity, we'll use a global in-memory list to simulate persistent storage. In a real application, this would be a database or a dedicated task management API.

```python
# ... (previous code for imports and setup) ...

# ---
Simple In-Memory Task Storage (Simulated Long-Term Memory) ---
---
tasks = []

@function_tool
def add_task(description: str, due_date: str = "No due date") -> str:
    """Adds a new task to the task list.

    Args:
        description: A brief description of the task.
        due_date: Optional due date for the task (e.g., "tomorrow", "2025-12-31").

    Returns:
        A confirmation message.
    """
    task_id = len(tasks) + 1
    tasks.append({"id": task_id, "description": description, "due_date": due_date, "completed": False})
    return f"Task '{description}' added with ID {task_id}. Due: {due_date}."

@function_tool
def list_tasks(status: str = "all") -> str:
    """Lists tasks based on their completion status.

    Args:
        status: Filter tasks by "all", "completed", or "pending". Defaults to "all".

    Returns:
        A string listing the tasks.
    """
    filtered_tasks = []
    if status == "completed":
        filtered_tasks = [t for t in tasks if t["completed"]]
    elif status == "pending":
        filtered_tasks = [t for t in tasks if not t["completed"]]
    else:
        filtered_tasks = tasks

    if not filtered_tasks:
        return f"No {status} tasks found."

    task_strings = []
    for t in filtered_tasks:
        task_strings.append(f"ID {t["id"]}: {t["description"]} (Due: {t["due_date"]}, Status: {'Completed' if t["completed"] else 'Pending'})")
    return "\n".join(task_strings)

@function_tool
def complete_task(task_id: int) -> str:
    """Marks a task as completed.

    Args:
        task_id: The ID of the task to complete.

    Returns:
        A confirmation message or error if task not found.
    """
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return f"Task '{task["description"]}' (ID {task_id}) marked as completed."
    return f"Task with ID {task_id} not found."

print("Task management tools defined.")
```

### Step 3: Define the Voice-Enabled Task Manager Agent

Now, create your `Agent` instance and provide it with the task management tools.

```python
# ... (previous code for imports, setup, and tools) ...

task_manager_agent = Agent(
    name="VoiceTaskManager",
    instructions=(
        "You are a voice-enabled task manager. "
        "You can add tasks, list tasks, and mark tasks as complete. "
        "Use the provided tools to manage tasks. "
        "Always confirm actions verbally and provide clear responses. "
        "If a task ID is needed, ask the user for it. "
    ),
    tools=[add_task, list_tasks, complete_task]
)

print("Voice-Enabled Task Manager Agent defined.")
```

### Step 4: Simulate Voice Interaction Loop

We'll create a simple loop to simulate a voice conversation with the agent.

```python
# ... (previous code for imports, setup, tools, and agent definition) ...

def run_voice_task_manager():
    print("\n--- Voice-Enabled Task Manager Ready ---\n")
    print("Say 'exit' to quit.")

    while True:
        user_input_text = input("You (type your voice command): ")
        if user_input_text.lower() == 'exit':
            print("Goodbye!")
            break

        # Simulate STT
        transcribed_command = conceptual_stt(user_input_text)

        # Run the agent
        result = Runner.run_sync(task_manager_agent, transcribed_command)
        agent_response_text = result.final_output

        # Simulate TTS
        spoken_response = conceptual_tts(agent_response_text)
        print(f"Agent: {spoken_response}\n")

# Run the manager
run_voice_task_manager()

print("\n--- Task Manager Session Ended ---")
print("Current tasks in memory:")
print(list_tasks())

```

---

## Key Takeaways from Project 3

*   You've built a **voice-enabled application** by conceptually integrating STT and TTS with an AI agent.
*   You've created **custom tools** to manage a simple task list, demonstrating how agents can interact with and persist data.
*   This project highlights the power of combining **natural language understanding** (via the agent) with **external actions** (via tools) and **persistent memory** (simulated in-memory list).
*   The `Runner` orchestrates the flow, allowing the agent to interpret voice commands and respond appropriately.

Congratulations on completing your third major project! This project showcases the practical application of voice interfaces and data management with AI agents. Tomorrow, we'll explore **Model Routing and Selection**, learning how to dynamically choose the most appropriate LLM for a given query.
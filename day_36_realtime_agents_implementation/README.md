# Day 36: `Realtime` Agents Implementation

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 36 of the **OpenAI Agent SDK Mastery** course! On Day 26, we introduced the foundational concepts of Realtime Agents and the challenges of achieving low latency. Today, we put that theory into practice by **implementing a low-latency agent** designed for live chat scenarios. You'll learn how to leverage asynchronous programming, streaming outputs, and efficient tool usage to create an agent that feels highly responsive and interactive. This session will focus on the practical code structures and considerations necessary to minimize perceived delays and deliver a fluid user experience, making your agents suitable for applications like customer support chatbots or interactive virtual assistants.

---

## Recap: Pillars of Realtime Agents

To achieve a truly real-time experience, we need to focus on minimizing latency at every stage of the agent's operation. Key techniques include:

*   **Streaming Outputs:** Delivering partial responses as they are generated (Day 9).
*   **Asynchronous Programming:** Using `asyncio` to prevent blocking operations and handle multiple tasks concurrently.
*   **Efficient Tool Usage:** Optimizing tool execution time and potentially running tools in parallel.
*   **Optimized LLM Inference:** (Conceptual) Using faster models, caching (Day 33), or other model-level optimizations.

Today, our primary focus will be on streaming and asynchronous execution within the context of the OpenAI Agents SDK.

---

## Leveraging `Runner.run_streamed()` for Responsiveness

The `Runner.run_streamed()` method is the cornerstone of building responsive agents. It allows you to receive `RunItem` events as they occur, enabling you to display partial responses to the user immediately, rather than waiting for the entire `final_output`.

### How it Enhances Realtime Experience:

*   **Perceived Latency Reduction:** Users see text appearing character by character or word by word, making the wait feel shorter.
*   **Immediate Feedback:** Tool calls and other internal agent actions can be displayed, providing transparency.
*   **Interactive Control:** In advanced scenarios, users might be able to interrupt or modify the agent's response mid-stream.

---

## Asynchronous Programming with `asyncio`

For truly non-blocking and scalable real-time applications (like web servers or complex UIs), asynchronous programming with Python's `asyncio` library is essential. It allows your application to perform other tasks while waiting for I/O-bound operations (like LLM API calls or external tool executions) to complete.

*   **`Runner.run()`:** This is the asynchronous counterpart to `Runner.run_sync()`. It returns a coroutine that must be `await`ed.
*   **`async` and `await`:** Keywords used to define and call asynchronous functions.

---

## Practical Implementation: A Realtime Chat Agent

Let's build a simple chat agent that uses streaming and asynchronous operations to provide a responsive experience.

```python
import asyncio
import os
from agents import Agent, Runner
from agents.tools import function_tool

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define a simple tool that simulates a delay (e.g., an API call)
@function_tool
async def delayed_lookup(query: str) -> str:
    """Simulates a time-consuming lookup operation."
    print(f"\n[TOOL]: Performing delayed lookup for '{query}'...")
    await asyncio.sleep(3) # Simulate 3 seconds of network latency or computation
    return f"Data for '{query}' retrieved successfully after a delay."

# Define the Realtime Agent
realtime_agent = Agent(
    name="RealtimeChatAgent",
    instructions=(
        "You are a highly responsive chat assistant. "
        "Answer user questions concisely. "
        "If the user asks for a 'delayed lookup', use the 'delayed_lookup' tool. "
        "Provide streaming output for a better user experience." 
    ),
    tools=[delayed_lookup]
)

async def chat_session():
    print("\n--- Realtime Chat Agent Ready ---\\n")
    print("Type your message. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        print("Agent: ", end="", flush=True)
        # Use run_streamed for real-time output
        with Runner.run_streamed(realtime_agent, user_input) as stream:
            async for event in stream:
                if hasattr(event, 'text'):
                    print(event.text, end="", flush=True) # Print LLM text as it arrives
                elif hasattr(event, 'tool_name'):
                    print(f"\n[Agent is using tool: {event.tool_name}]
", end="", flush=True)
                elif hasattr(event, 'output'):
                    print(f"\n[Tool output: {event.output}]", end="", flush=True)
            
            # After streaming, get the final result if needed
            final_result = stream.get_final_result()
            # print(f"\n(Final result received: {final_result.final_output[:50]}...)")
        print("\n") # Newline after agent's full response

if __name__ == "__main__":
    asyncio.run(chat_session())

```

**Explanation:**

*   The `delayed_lookup` tool is an `async` function, simulating an I/O bound operation. This allows the `Runner` to continue processing other tasks while waiting for the tool to complete.
*   The `chat_session` function is an `async` function, allowing us to use `await` and `async for`.
*   `Runner.run_streamed()` is used within an `async for` loop to process events as they are yielded by the agent.
*   `print(event.text, end="", flush=True)` ensures that text is printed immediately without buffering, creating the real-time typing effect.
*   Messages indicating tool usage and output are printed to show the agent's internal process in real-time.

---

## Key Considerations for Realtime Implementation

*   **Asynchronous Tooling:** Ensure any custom tools that perform I/O operations (API calls, database queries, file I/O) are implemented asynchronously (`async def`) to avoid blocking the event loop.
*   **Perceived vs. Actual Latency:** Streaming primarily reduces *perceived* latency. Actual end-to-end latency might still be high if LLM inference or tool execution is slow. Optimize these components where possible.
*   **Error Handling:** Implement robust error handling within your `async for` loops to gracefully manage exceptions during streaming.
*   **Resource Management:** Be mindful of resource consumption, especially in high-throughput scenarios. Consider connection pooling for external services.
*   **User Experience:** Design your UI to effectively display streaming output and provide clear indicators of agent activity (e.g., "Agent is thinking...", "Agent is searching...").

---

## Key Takeaways

*   **Realtime Agent Implementation** focuses on minimizing latency for responsive user experiences.
*   **`Runner.run_streamed()`** is crucial for delivering partial outputs and events in real-time.
*   **Asynchronous programming (`asyncio`)** is essential for building non-blocking, scalable real-time applications.
*   Implementing asynchronous custom tools helps prevent blocking the event loop during I/O operations.
*   Optimizing both perceived and actual latency is key for successful real-time agent deployment.

Today, you've built a responsive, real-time agent. Tomorrow, we'll extend this further by implementing **Voice Agents**, integrating speech-to-text and text-to-speech for truly natural, spoken interactions.
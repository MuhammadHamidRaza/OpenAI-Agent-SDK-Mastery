# Day 3: Understanding `Runner` and Basic Execution

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 3 of the **OpenAI Agent SDK Mastery** course! Having explored the foundational concepts of AI agents and the agent loop, today we delve into the crucial component responsible for executing your agents: the `Runner` class. We'll explore its various methods—`run_sync()`, `run()`, and `run_streamed()`—understanding when and how to use each for different execution scenarios. By the end of today, you'll be proficient in running your agents effectively, whether for simple scripts, asynchronous applications, or real-time streaming interfaces.

---

## What is the `Runner` Class?

The `Runner` class in the OpenAI Agents SDK is the primary interface for executing agents. It orchestrates the agent loop, managing the flow of information between the agent, its tools, and the session. Essentially, the `Runner` takes an agent and an input, then drives the agent through its reasoning and action steps until a final output is produced or a predefined limit (like `max_turns`) is reached.

It abstracts away the complexities of the underlying agentic process, providing a simple and consistent API for developers to interact with their AI agents.

---

## `Runner` Methods for Agent Execution

The `Runner` class provides several methods to execute agents, each suited for different programming contexts and requirements.

### `Runner.run_sync()`: Synchronous Execution

*   **What it is:** This is a synchronous (blocking) method that executes the agent and returns the `RunResult` once the agent has completed its task. It's a convenient wrapper around the asynchronous `Runner.run()` method.
*   **When to use it:** Ideal for simple scripts, command-line interfaces (CLIs), local testing, and environments where asynchronous programming is not required or desired. It's the easiest way to get started and see immediate results.
*   **Example:**

    ```python
    from agents import Agent, Runner
    import os

    # Ensure the OpenAI API key is set (replace with your actual key or set as environment variable)
    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

    if "OPENAI_API_KEY" not in os.environ:
        print("Please set the OPENAI_API_KEY environment variable.")
        exit()

    # Define a simple agent
    agent = Agent(
        name="GreetingAgent",
        instructions="You are a friendly assistant that greets users."
    )

    # Run the agent synchronously
    print("Running agent synchronously...")
    result = Runner.run_sync(agent, "Hello there!")

    # Print the final output
    print("Agent's response:", result.final_output)
    ```

### `Runner.run()`: Asynchronous Execution

*   **What it is:** This is the core asynchronous method for executing agents. It returns a `RunResult` object, but it must be `await`ed within an `async` function.
*   **When to use it:** Best suited for asynchronous programming environments such as web servers (e.g., FastAPI, Aiohttp), asynchronous notebooks, or any application where non-blocking operations are crucial for performance and responsiveness.
*   **Example:**

    ```python
    import asyncio
    from agents import Agent, Runner
    import os

    # Ensure the OpenAI API key is set
    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

    if "OPENAI_API_KEY" not in os.environ:
        print("Please set the OPENAI_API_KEY environment variable.")
        exit()

    async def main():
        # Define a simple agent
        agent = Agent(
            name="AsyncAgent",
            instructions="You are an agent that provides short, concise answers."
        )

        # Run the agent asynchronously
        print("Running agent asynchronously...")
        result = await Runner.run(agent, "What is the capital of France?")

        # Print the final output
        print("Agent's response:", result.final_output)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

### `Runner.run_streamed()`: Streaming Execution

*   **What it is:** This method allows you to receive intermediate events and partial outputs from the agent as it processes the request. It returns a `RunResultStreaming` object, which can be iterated over to get real-time updates.
*   **When to use it:** Ideal for building interactive chat UIs, progress indicators, or any application where you want to provide immediate feedback to the user as the agent "thinks" or generates its response. It enhances the user experience by reducing perceived latency.
*   **Example (Conceptual):**

    ```python
    from agents import Agent, Runner
    import os

    # Ensure the OpenAI API key is set
    # os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

    if "OPENAI_API_KEY" not in os.environ:
        print("Please set the OPENAI_API_KEY environment variable.")
        exit()

    # Define a simple agent
    agent = Agent(
        name="StreamerAgent",
        instructions="You are an agent that provides a detailed explanation step-by-step."
    )

    print("Running agent with streaming...")
    with Runner.run_streamed(agent, "Explain the concept of recursion in programming.") as stream:
        for event in stream:
            # Process each event as it comes in
            if hasattr(event, 'text'): # Check if the event has a 'text' attribute (e.g., MessageOutputItem)
                print(event.text, end="", flush=True) # Print partial text
            # You can also check for other event types like ToolCallItem, ReasoningItem etc.
        
        # After the stream is complete, you can get the final result
        final_result = stream.get_final_result()
        print("

Final output received via streaming:", final_result.final_output)
    ```
    *Note: The `run_streamed` example above is conceptual and demonstrates how you might process events. The actual `event` objects will be instances of `RunItem` subclasses (e.g., `MessageOutputItem`, `ToolCallItem`). You would typically check the type of `event` to handle different kinds of updates.*

---

## Key Takeaways

*   The `Runner` class is your gateway to executing agents in the OpenAI Agents SDK.
*   Choose `Runner.run_sync()` for quick scripts and local testing.
*   Opt for `Runner.run()` in asynchronous applications for non-blocking execution.
*   Utilize `Runner.run_streamed()` to provide real-time feedback and enhance user experience in interactive applications.
*   Always ensure your `OPENAI_API_KEY` is securely set as an environment variable before running agents.

By mastering the `Runner` class, you gain full control over how your agents operate and integrate into various application architectures.
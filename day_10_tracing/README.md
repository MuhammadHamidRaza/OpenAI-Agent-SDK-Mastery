# Day 10: Tracing for Observability

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 10 of the **OpenAI Agent SDK Mastery** course! As your agents become more complex, understanding their internal decision-making process is crucial. Today, we'll explore **Tracing**, a powerful feature in the OpenAI Agents SDK that provides deep visibility into your agent's workflow. Tracing allows you to visualize and debug every step an agent takes, from receiving a prompt to calling tools and generating responses.

---

## What is Tracing?

Tracing is like a flight recorder for your agent. It captures a detailed, step-by-step timeline of an agent's run, including LLM generations, tool calls, and other significant events. This is essential for:

*   **Debugging:** Pinpoint exactly where a run went wrong.
*   **Understanding:** Inspect how the agent reasoned and which tools it called.
*   **Optimizing:** Identify and remove unnecessary or slow steps.
*   **Auditing:** Keep a history of decisions for review.

Traces are composed of **Spans**, which are individual operations within the workflow, like an agent run, a tool call, or an LLM generation.

## How to View Traces

By default, the OpenAI Agents SDK is configured to send traces to the OpenAI platform. You can view these traces in your [OpenAI Traces Dashboard](https://platform.openai.com/traces). Each run of an agent will generate a trace that you can inspect in the dashboard.

## How to Disable Tracing

Tracing is enabled by default. If you need to disable it, you have two options:

**1. Disable Tracing for a Single Run:**

You can disable tracing for a specific run by passing a `RunConfig` object to the `Runner`.

```python
from agents import Agent, Runner, RunConfig

agent = Agent(
    name="MyAgent",
    instructions="You are a helpful assistant."
)

# This run will not be traced
result = Runner.run_sync(
    agent,
    "Hello, world!",
    run_config=RunConfig(tracing_disabled=True)
)
```

**2. Disable Tracing Globally:**

You can disable tracing for all runs by setting the `OPENAI_AGENTS_DISABLE_TRACING` environment variable to `1`.

```bash
export OPENAI_AGENTS_DISABLE_TRACING=1
```

## Basic Tracing Example

When you run an agent, the SDK automatically traces the execution. Let's look at a simple example of an agent that uses a tool.

```python
from agents import Agent, Runner
from agents.tools import function_tool
import os

# Make sure to set your OPENAI_API_KEY
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

@function_tool
def get_weather(city: str) -> str:
    """Gets the current weather for a specified city."""
    if "san francisco" in city.lower():
        return "Sunny and 75 degrees."
    else:
        return "I'm sorry, I don't have the weather for that city."

weather_agent = Agent(
    name="WeatherAgent",
    instructions="You are a helpful assistant that can provide weather information.",
    tools=[get_weather]
)

result = Runner.run_sync(weather_agent, "What's the weather in San Francisco?")

print(f"Final Output: {result.final_output}")

```

When you run this code, you can go to your [OpenAI Traces Dashboard](https://platform.openai.com/traces) to see the full trace of the execution, including the tool call to `get_weather`.

## Custom Traces and Spans

You can also create your own custom traces and spans to group related operations and track specific information.

### Custom Traces with `trace()`

The `trace()` context manager allows you to group multiple agent runs into a single, higher-level trace.

```python
import asyncio
from agents import Agent, Runner, trace

async def main():
    agent = Agent(name="JokeAgent", instructions="Tell me a joke.")

    with trace("JokeWorkflow"):
        # First run
        result1 = await Runner.run(agent, "Tell me a joke about cats.")
        print(f"Joke: {result1.final_output}")

        # Second run, grouped in the same trace
        result2 = await Runner.run(agent, "Now tell me one about dogs.")
        print(f"Joke: {result2.final_output}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Custom Spans with `span()`

The `span()` context manager allows you to create custom spans within a trace to track specific operations.

```python
import asyncio
from agents import Agent, Runner, trace, span

async def main():
    agent = Agent(name="MyAgent", instructions="You are a helpful assistant.")

    with trace("MyWorkflow"):
        with span("MyCustomSpan"):
            # Your custom logic here
            print("This is a custom span.")

        await Runner.run(agent, "Hello, world!")

if __name__ == "__main__":
    asyncio.run(main())
```

## External Tracing Providers

The OpenAI Agents SDK also supports sending traces to external providers like LangSmith, Weights & Biases, and others. This allows you to integrate the SDK's tracing capabilities with your existing observability tools. You can find more information about this in the official documentation.

---

Today, you've learned how to use tracing to gain visibility into your agent's execution. This is a critical skill for debugging, optimizing, and ensuring the reliability of your agentic applications. Tomorrow, we'll start our first project: building a **Simple Q&A Agent**.
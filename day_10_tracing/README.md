


# Day 10: Tracing for Observability

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 10 of the **OpenAI Agent SDK Mastery** course! As agents become more sophisticated, their internal decision-making processes can become complex and opaque. Today, we tackle this challenge by diving into **Tracing**, a powerful feature within the OpenAI Agents SDK that provides deep visibility into your agent's workflow. Tracing allows you to visualize and understand every step an agent takes—from receiving a prompt, to making decisions, calling tools, and generating responses. This session will equip you with essential debugging and optimization skills, enabling you to fine-tune your agents and ensure they behave as expected.

---

## The Need for Observability in Agentic Systems

Unlike traditional software, where execution paths are often explicit and predictable, agentic systems powered by Large Language Models (LLMs) can exhibit emergent behaviors. The LLM's internal reasoning process, its choice of tools, and the sequence of actions can sometimes be difficult to anticipate or debug. This "black box" nature makes observability crucial.

**Observability** in the context of AI agents refers to the ability to understand the internal state of the system by examining its outputs. Tracing is a key component of achieving this observability. It provides a detailed, step-by-step record of an agent's execution, allowing developers to:

*   **Debug Effectively:** Pinpoint exactly where an agent went wrong, whether it's a misunderstanding of the prompt, an incorrect tool selection, or an issue with tool output processing.
*   **Understand Agent Behavior:** Gain insights into how the LLM interprets instructions and makes decisions.
*   **Optimize Performance:** Identify bottlenecks or inefficient reasoning paths.
*   **Ensure Reliability:** Verify that the agent is following the intended logic and not deviating unexpectedly.

---

## How Tracing Works in the OpenAI Agents SDK

The OpenAI Agents SDK provides built-in tracing capabilities that automatically record the sequence of events during an agent's run. These events are typically captured as `RunItem` objects (which we explored on Day 9) and can be visualized or logged for analysis.

While the SDK handles the collection of these traces, the visualization aspect often depends on integration with external tools or a custom UI. However, the raw `RunItem` stream (from `run_streamed()`) or the `new_items` property of `RunResult` already contain all the necessary information for tracing.

### Key Elements Captured by Tracing:

*   **Input/Output:** The initial prompt, intermediate messages from the LLM, and the final response.
*   **Tool Calls:** When a tool is invoked, which tool, and with what arguments.
*   **Tool Outputs:** The results returned by the executed tools.
*   **Reasoning Steps:** In some configurations, the LLM's internal thought process or reasoning steps can also be captured.
*   **Handoffs:** In multi-agent systems, tracing records when control is passed from one agent to another.

### Conceptual Example: Visualizing a Trace

Imagine a simple agent that uses a `WebSearchTool` to answer a question. A trace of its execution might look like this:

1.  **User Input:** "What is the capital of Australia?"
2.  **LLM Thought:** "The user is asking a factual question that requires external knowledge. I should use the `WebSearchTool`."
3.  **Tool Call:** `WebSearchTool(query="capital of Australia")`
4.  **Tool Output:** "Canberra"
5.  **LLM Thought:** "The web search returned 'Canberra'. I should formulate a polite answer."
6.  **LLM Message:** "The capital of Australia is Canberra."
7.  **Final Output:** "The capital of Australia is Canberra."

This sequence of events, captured by the SDK, provides a clear narrative of how the agent arrived at its answer.

---

## Practical Aspects of Tracing

While the SDK collects the trace data, how you consume and visualize it depends on your needs:

### 1. Programmatic Inspection (using `RunResult`)

As seen on Day 9, you can iterate through `result.new_items` to programmatically inspect the sequence of events. This is useful for logging, custom analytics, or simple console-based debugging.

```python
from agents import Agent, Runner
from agents.tools import WebSearchTool # Assuming this is available
import os

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Initialize WebSearchTool (conceptual, requires actual setup)
# web_search_tool = WebSearchTool()

agent = Agent(
    name="FactChecker",
    instructions="You answer factual questions using web search.",
    # tools=[web_search_tool] # Uncomment if WebSearchTool is properly configured
)

print("Running agent with tracing inspection...")
# For demonstration, let's assume the agent can answer without a tool if no tool is provided
# In a real scenario, you'd ensure the tool is available and used.
result = Runner.run_sync(agent, "What is the largest ocean on Earth?")

print("\n--- Agent Trace ---")
for i, item in enumerate(result.new_items):
    print(f"Step {i+1}: {type(item).__name__}")
    if hasattr(item, 'text'):
        print(f"  Message: {item.text[:100]}...")
    if hasattr(item, 'tool_name'):
        print(f"  Tool Call: {item.tool_name}({item.tool_args})")
    if hasattr(item, 'output'):
        print(f"  Tool Output: {item.output[:100]}...")
    # Add more conditions for other RunItem types as needed

print(f"\nFinal Output: {result.final_output}")

```

### 2. Integration with Observability Platforms

For production-grade applications, you would typically integrate the SDK's tracing output with dedicated AI observability platforms (e.g., LangChain's LangSmith, Weights & Biases, or custom logging solutions). These platforms can:

*   **Visualize Traces:** Provide interactive UIs to view the flow of execution, including LLM calls, tool usage, and intermediate steps.
*   **Monitor Performance:** Track latency, token usage, and cost.
*   **Evaluate Agent Quality:** Help in A/B testing different agent versions and evaluating their responses.
*   **Store Historical Traces:** Maintain a record of all agent runs for auditing and analysis.

---

## Key Takeaways

*   **Tracing** is vital for understanding, debugging, and optimizing complex AI agent behaviors.
*   It provides a detailed, step-by-step record of an agent's execution, including inputs, outputs, tool calls, and reasoning.
*   The OpenAI Agents SDK automatically captures trace data as `RunItem` objects.
*   You can programmatically inspect traces using the `RunResult` object's `new_items` property or integrate with external observability platforms for advanced visualization and monitoring.

With tracing, you gain unprecedented insight into the "mind" of your agent, transforming the black box into a transparent and manageable system. Tomorrow, we'll apply much of what we've learned by embarking on our first major project: building a **Simple Q&A Agent**.

Day 10 — Tracing & Observability (complete, with tools & multi-agent examples)

Goal: give you a single, correct, production-ready Day 10 lesson on tracing for the OpenAI Agents SDK. This file explains what tracing is, why it matters, and provides clean, copy-paste examples that include tools and multi-agent handoffs. Replace environment variables / model clients as needed for your environment.

TL;DR — What is tracing?

Tracing is the flight recorder for agentic systems. It records a step-by-step timeline of an agent run (LLM generations, tool calls, handoffs, spans). Use traces to:

Debug — find exactly where a run went wrong.

Understand — inspect how the agent reasoned and which tools it called.

Optimize — spot heavy/slow spans and remove unnecessary steps.

Audit — keep an auditable history of decisions (careful with PII).

Traces are composed of Traces (a workflow) and nested Spans (operations inside the workflow: agent run, generation, function call, etc.). The SDK collects traces by default; you can group runs with trace(...), inspect RunResult, and stream run events.

Quick checklist before running examples

Python 3.8+ and a virtual env.

Install SDK (example): pip install openai-agents python-dotenv

Add keys to .env (do not hardcode secrets):

OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...            # if you use Gemini/other client


If you want to export traces to OpenAI Traces Dashboard or other backends, configure the SDK per your platform docs.

1) Core concepts — useful RunResult fields

When you call the Runner you receive a RunResult (or RunResultStreaming for streamed runs). Key fields:

final_output — the final answer (string or structured object if agent had an output_type).

new_items — chronological list of RunItem objects (messages, tool call items, tool outputs, reasoning items, handoff items).

last_agent — the Agent instance that produced the final output (useful in handoffs).

input — the original input passed to the run.

raw_responses — low-level model responses (tokens, metadata).

to_input_list() — convert run history back into an input list to continue a conversation manually.

Guardrail results / metadata may also appear if configured.

2) Minimal tracing example (sync, tool usage, inspect RunResult)
# day10_calculator_sync.py
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.tools import function_tool
from openai import AsyncOpenAI  # used as a model client wrapper (example)

if "GEMINI_API_KEY" not in os.environ:
    raise RuntimeError("GEMINI_API_KEY not set in .env (or set OPENAI_API_KEY for OpenAI models)")

# Configure an async client for Gemini (example). Replace with your model client per SDK.
client = AsyncOpenAI(api_key=os.environ["GEMINI_API_KEY"], base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)

@function_tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the sum."""
    return a + b

calculator_agent = Agent(
    name="CalculatorAgent",
    instructions="You are a helpful assistant that performs arithmetic using the provided tools when helpful.",
    tools=[add_numbers],
    model=model
)

# Run the agent
res = Runner.run_sync(calculator_agent, "What is 123.45 + 67.89?")

print("Final output:", res.final_output)
print("\n-- New items (chronological):")
for i, item in enumerate(res.new_items or []):
    print(f"{i+1}. {type(item).__name__}")
    # Many RunItem types expose text/tool fields depending on SDK version:
    if hasattr(item, "text"):
        print("   text:", item.text)
    if hasattr(item, "tool_name"):
        print("   tool_name:", item.tool_name, "args:", getattr(item, "tool_args", None))
    if hasattr(item, "output"):
        print("   tool output:", item.output)


What this shows

The RunResult contains the final answer.

new_items will include ToolCallItem and ToolCallOutputItem entries showing the tool call and its output — perfect for tracing and auditing.

3) Async example with trace grouping (group several runs into one workflow)
# day10_grouped_trace_async.py
import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from agents import Agent, Runner, trace

async def main():
    agent = Agent(name="JokeMaker", instructions="Tell short, clean jokes.")
    # Wrap related runs in one trace (useful to correlate them in dashboard)
    with trace("joke_workflow", metadata={"course_day": 10}):
        r1 = await Runner.run(agent, "Tell me a short joke about computers.")
        print("Joke:", r1.final_output)

        r2 = await Runner.run(agent, f"Rate this joke: {r1.final_output}")
        print("Rating:", r2.final_output)

if __name__ == "__main__":
    asyncio.run(main())


Why group runs? the trace groups multiple Runner.run calls into a single trace workflow so you can see the entire conversation / steps together.

4) Streaming example — get events in real time

Two useful streaming views:

raw token deltas (token-by-token),

higher-level run-item events (message/tool completed).

# day10_streaming_example.py
import asyncio
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from agents import Agent, Runner

async def main():
    agent = Agent(name="Streamer", instructions="Explain one step at a time.")
    # Get a streaming RunResult
    streaming_result = Runner.run_streamed(agent, "Explain photosynthesis in simple terms.")

    # Use the provided stream_events() async iterator to receive events
    async for ev in streaming_result.stream_events():
        # raw LLM deltas (token-by-token)
        if ev.type == "raw_response_event":
            # event.data.delta or similar shape depending on SDK version
            data = getattr(ev, "data", None)
            delta = getattr(data, "delta", None)
            if delta:
                print(delta, end="", flush=True)
        # higher-level completed items
        elif ev.type == "run_item_stream_event":
            item = ev.item
            print(f"\n[ITEM COMPLETED] {item.type}: {getattr(item, 'text', getattr(item,'output', None))}")

    final = streaming_result.get_final_result()
    print("\n\nFinal:", final.final_output)

if __name__ == "__main__":
    asyncio.run(main())


Use case: show partial responses in a chat UI and record the trace/steps for auditing.

5) Multi-agent example (triage → specialist handoff)

You asked for agents and handoffs — here’s a compact example that shows a triage_agent that delegates to either history_tutor_agent or math_tutor_agent depending on the question. (The actual handoff behavior depends on the SDK's handoff implementation — below uses handoffs argument.)

# day10_multi_agent_handoff.py
import asyncio
from agents import Agent, Runner, trace

# specialist agents
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You are a history expert. Answer historical questions clearly with dates and context."
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You are a math expert. Show the steps when solving problems and give examples."
)

# triage agent chooses which specialist to use
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "You are a triage agent. Read the user's homework question and decide whether the "
        "question should go to History Tutor or Math Tutor. If it's math, hand off to Math Tutor; "
        "if it's historical or about events, hand off to History Tutor. Provide a short reason for the handoff."
    ),
    handoffs=[history_tutor_agent, math_tutor_agent]
)

async def run_handoff_example(question: str):
    # Wrap in a trace so we can see the handoff sequence in one trace
    with trace("multi_agent_handoff_example", metadata={"question": question[:60]}):
        res = await Runner.run(triage_agent, question)
        print("Triage final output:", res.final_output)
        # If the SDK supports `res.last_agent`, it may indicate which agent produced the final result:
        print("Last agent:", getattr(res, "last_agent", None))

if __name__ == "__main__":
    # math question -> should route to Math Tutor
    asyncio.run(run_handoff_example("Solve: 12 * (4 + 3)"))
    # history question -> should route to History Tutor
    asyncio.run(run_handoff_example("When did the Battle of Hastings happen?"))


Note: actual handoff behavior (how to trigger another agent) is SDK specific — the handoffs field is the concept. The trace will show which agent(s) ran. Inspect res.new_items / res.last_agent to confirm which agent produced the final answer.

6) Programmatic inspection of a RunResult (post-run trace)

After a run you can inspect the run items to build logs or visualizations:

# day10_inspect.py
from agents import Agent, Runner

agent = Agent(name="Inspector", instructions="Answer briefly.")

res = Runner.run_sync(agent, "What is the tallest mountain?")

print("Final:", res.final_output)
print("Last agent:", getattr(res, "last_agent", None))

print("\nNew items (chronological):")
for n, item in enumerate(res.new_items or [], start=1):
    print(f"{n}. {type(item).__name__}")
    if hasattr(item, "text"):
        print("   text:", item.text)
    if hasattr(item, "tool_name"):
        print("   tool_name:", item.tool_name, "args:", getattr(item, "tool_args", None))
    if hasattr(item, "output"):
        print("   output:", item.output)

7) Custom trace processors / exporting to other observability systems

The SDK exposes hooks to add or replace trace processors so you can export traces to LangSmith, W&B, MLflow, or your internal system. The API names can vary by SDK version (add_trace_processor, set_trace_processors). Use them at app startup.

Conceptual pattern:

from agents import add_trace_processor

class MyTraceProcessor:
    def export(self, trace):
        # transform and send trace to your backend
        send_to_my_backend(transform(trace))

add_trace_processor(MyTraceProcessor())

8) Sensitive data & privacy

Traces can include LLM inputs/outputs and function call args — potentially sensitive.

Use SDK options to exclude sensitive content (e.g., RunConfig.trace_include_sensitive_data = False) or redact data before run.

For regulated environments enable retention & encryption policies or disable tracing entirely.

9) Disable tracing (temporary / global)

Global (env): export OPENAI_AGENTS_DISABLE_TRACING=1

Per-run: use RunConfig(tracing_disabled=True) when calling Runner if your SDK supports it.

Day 03 — Understanding Runner & Basic Execution

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

  

---

  

### **Course Overview**

  
  

Welcome to Day 3 of the **OpenAI Agent SDK Mastery** course! 🚀

In the last two days, you built your first agent and explored how the **Agent Loop** and **Sessions** power its intelligence. Today, we’ll focus on the **Runner**—the engine that actually runs your agent and executes tasks.

  

Think of the Runner as the **conductor of an orchestra**: it coordinates the agent’s thinking, ensures smooth execution, and decides how inputs and outputs flow. We’ll explore:

  

- The different **execution modes** (sync, async, streaming).

- How to use the `Runner` to run agents step-by-step.

- Writing simple programs to test and debug your agent.

  

By the end of today, you’ll not only understand how the Runner works under the hood but also learn how to **control execution flow**, making your agents faster, smarter, and more reliable.

---

  

## TL;DR

  

-  `Runner.run(...)` — **async**, use `await` inside `async def`. Returns a `RunResult`.

-  `Runner.run_sync(...)` — **sync (blocking)** wrapper around `run` for scripts/CLIs. Returns a `RunResult`.

-  `Runner.run_streamed(...)` — **streams events** (partial tokens, tool calls). Returns `RunResultStreaming`; use `result.stream_events()` to iterate.

  

---

  

## Objectives

  

1. Run agents in sync, async, and streaming modes.

2. Know which Runner method to use and why.

3. Use `async` / `await` and `asyncio` patterns with the SDK.

4. Inspect `RunResult` / `RunResultStreaming` for debugging.

  

---

  

## 1) What is the Runner?

  

The **`Runner`** class is the main entry point for executing your agent. It’s responsible for:

-   Starting the agent loop.
    
-   Passing the prompt to the agent.
    
-   Handling tool calls and handoffs.
    
-   Returning the final result.
  

---

  

## 2) The three Runner methods (short + copy-paste)

  

### A — `Runner.run(...)` (async)

Use this inside async applications (FastAPI, async workers). It does **not** block the event loop.

  

```python

# async_run.py

import asyncio

from agents import Agent, Runner

  

async  def  main():

agent = Agent(name="Assistant", instructions="Answer concisely.")

result = await Runner.run(agent, "Write a haiku about recursion in programming.")

print("Final Output:", result.final_output)

  

if  __name__ == "__main__":

asyncio.run(main())

```

  

**When to use:** web servers, background async tasks, concurrent runs.

  
  

### B — `Runner.run_sync(...)` (blocking)

A simple wrapper for scripts and CLIs. It blocks until the run completes — **do not** call inside an already-running event loop.

  

```python

# sync_run.py

from agents import Agent, Runner

  

agent = Agent(name="Assistant", instructions="Answer concisely.")

result = Runner.run_sync(agent, "Explain recursion in one short sentence.")

print("Final Output:", result.final_output)

```

  

**When to use:** small scripts, cron jobs, local testing.

  
  

### C — `Runner.run_streamed(...)` (streaming)

Use this when you want live updates (token-by-token, tool call starts/ends). `run_streamed` returns a `RunResultStreaming`. Iterate `async for` over `result.stream_events()` to receive streaming events. After the stream completes the `RunResultStreaming` object contains the full run results (headers, raw responses, new items, and `final_output`).

  

```python

# streamed_run.py

import asyncio

from agents import Agent, Runner

from openai.types.responses import ResponseTextDeltaEvent

  

async  def  main():

# make sure `model` is defined (string or model provider object) if you pass it here

agent = Agent(name="Streamer", instructions="Give three quick tips.")

result = Runner.run_streamed(agent, input="Give three study tips for today.")

  

async  for event in result.stream_events():

# Example: token deltas

if event.type == "raw_response_event"  and  isinstance(event.data, ResponseTextDeltaEvent):

print(event.data.delta, end="", flush=True)

  

# After the stream ends the RunResultStreaming object contains the final output

print("

Final Output:", result.final_output)

  

if  __name__ == "__main__":

asyncio.run(main())

```

  

**When to use:** chat UIs, progress bars, observability and debugging.

  

---

  

## 3) RunResult & RunResultStreaming (quick)

  

-  `RunResult` (from `run` / `run_sync`): contains `final_output`, `last_agent`, `new_items`, and helper methods like `to_input_list()`.

-  `RunResultStreaming` (from `run_streamed`): provides `stream_events()` (an async iterator of stream events). Once the stream completes the `RunResultStreaming` also contains the final outputs and metadata (you can access `result.final_output`, `result.new_items`, `result.raw_responses`, etc.).

  

---

  

## 4) Results — details you should log / store

  

When you call the Runner methods, you get either:

  

-  **RunResult** → if you call `run` or `run_sync`

-  **RunResultStreaming** → if you call `run_streamed`

  

Both inherit from **RunResultBase**, which contains the most useful fields.

  

### Final output

-  `final_output`: the final output produced by the last agent. It is either a `str` (when no `output_type` defined) or an object of the agent's `output_type`. It is dynamically typed (`Any`) because handoffs can change which agent finishes the run.

  

### Inputs for the next turn

-  `to_input_list()`: merge original input with `new_items` so you can pass the run into a subsequent run (useful for multi-turn flows).

  

### Last agent

-  `last_agent`: the agent that produced the final output — useful for re-using the same agent on the next user input (e.g., a language-specific agent after a handoff).

  

### New items

-  `new_items`: list of `RunItem` objects created during the run. Typical types:

-  `MessageOutputItem` — message from the LLM.

-  `ToolCallItem` / `ToolCallOutputItem` — tool invocation and its response.

-  `HandoffCallItem` / `HandoffOutputItem` — handoff tooling between agents.

-  `ReasoningItem` — internal reasoning or chain-of-thought items (if emitted).

  

### Guardrails, raw responses, and original input

-  `input_guardrail_results` and `output_guardrail_results` — guardrail checks (log/store if relevant).

-  `raw_responses` — low-level ModelResponses from the LLM (for audits).

-  `input` — the original input provided to the run.

  

---

  

## 5) Streaming events — two useful levels

  

1.  **Raw response events** (`raw_response_event`, `ResponseTextDeltaEvent`) — low-level token deltas from the Responses API. Use for token-by-token UIs.

2.  **Run item & agent events** (`run_item_stream_event`, `agent_updated_stream_event`) — higher-level, semantic events such as "message completed", "tool called", or "agent changed". Use for friendly progress messages ("Fetching calendar...").

  

**Raw token streaming example** — prints tokens as they arrive (see earlier example).

  

**Run item streaming example** — shows higher-level updates (tool calls, message completions):

  

```python

# run_item_stream.py

import asyncio

import random

from agents import Agent, ItemHelpers, Runner, function_tool

  

@function_tool

def  how_many_jokes() -> int:

return random.randint(1, 10)

  

async  def  main():

agent = Agent(

name="Joker",

instructions="First call the `how_many_jokes` tool, then tell that many jokes.",

tools=[how_many_jokes],

)

  

result = Runner.run_streamed(agent, input="Hello")

print("=== Run starting ===")

  

async  for event in result.stream_events():

if event.type == "raw_response_event":

continue  # ignore raw token deltas

elif event.type == "agent_updated_stream_event":

print(f"Agent updated: {event.new_agent.name}")

elif event.type == "run_item_stream_event":

if event.item.type == "tool_call_item":

print("-- Tool was called")

elif event.item.type == "tool_call_output_item":

print(f"-- Tool output: {event.item.output}")

elif event.item.type == "message_output_item":

print(f"-- Message output:

{ItemHelpers.text_message_output(event.item)}")

  

print("=== Run complete ===")

  

if  __name__ == "__main__":

asyncio.run(main())

```

  

> Note: streaming event ordering and timing can vary by model/provider and SDK version. In a few SDK integrations users have observed ordering differences for `run_item_stream_event` vs raw token deltas — keep this in mind when building UIs.

  

---

  

## 6) 🔹 Sync vs Async vs Asyncio in Python (quick recap)

  

**Synchronous (Sync)** — one task at a time, blocking. Good for CPU-heavy work.

  

```python

import time

  

def  task(name):

print(f"Starting {name}")

time.sleep(2)

print(f"Finished {name}")

  

task("Task 1")

task("Task 2")

```

  

**Asynchronous (Async)** — concurrent with `async`/`await`. Good for I/O-heavy work.

  

```python

import asyncio

  

async  def  task(name):

print(f"Starting {name}")

await asyncio.sleep(2)

print(f"Finished {name}")

  

async  def  main():

await asyncio.gather(task("Task 1"), task("Task 2"))

  

asyncio.run(main())

```

  

**Asyncio** — the event loop powering async code (used in FastAPI, aiohttp, etc.).

  

---

  

## 7) When to use which — one-line cues

  

-  `run_sync()` — **"Run and exit"** (scripts, cron).

-  `run()` — **"Await in servers"** (FastAPI, scalable apps).

-  `run_streamed()` — **"Show typing"** (chat UIs, debugging, progress).

  

---

  

## 8) Real-world patterns & short examples

  

-  **FastAPI per-request handler**: use `await Runner.run()` so the server stays responsive.

-  **CLI / nightly batch**: `Runner.run_sync()` for simple blocking scripts run by cron.

-  **Chat UI with live typing**: `Runner.run_streamed()` and forward `ResponseTextDeltaEvent` deltas via WebSocket/SSE.

-  **Parallel evaluation**: `await Runner.run()` within `asyncio.gather()` to run many prompts in parallel.

-  **Observability**: use `run_streamed()` to log `run_item_stream_event` and `agent_updated_stream_event` for audit and debugging.

  

---
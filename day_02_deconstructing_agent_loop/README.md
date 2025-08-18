# Day 02 — Deconstructing the Agent Loop & Sessions 

### **Course Overview**

Course Overview
Welcome to Day 2 of the **OpenAI Agent SDK Mastery** course! After building your first agent yesterday, today we’re diving into the engine that makes agents tick: the **Agent Loop** and **Sessions**. Think of the Agent Loop as the brain’s decision-making cycle and Sessions as the memory that keeps your agent from forgetting you. We’ll break it down in plain English with step-by-step explanations, copy-paste code, and real-world examples—like a pizza-ordering bot that remembers your favorite toppings or a study buddy that tracks your coding lessons. By the end, you’ll run agents in different modes (async, sync, streaming), manage multi-turn chats, and debug like a pro. Let’s make agents feel alive!

---



- **Agent Loop**: the SDK repeats a short cycle — *prepare input → model step → (maybe) action → repeat* — until a final answer.
- **Sessions**: persistent memory (e.g., `SQLiteSession`) so your agent remembers previous turns.
- **Runner**: three simple ways to run an agent: `run` (async), `run_sync()` (sync wrapper), and `run_streamed()` (streaming).
- **RunResult**: what you get back — `final_output`, `new_items`, `to_input_list()`.

---

# 1 — Key quick definitions (one line each)

- **Agent**: an LLM configured with a `name`, `instructions`, and optional `tools`.
- **Runner**: the executor that runs the agent and returns results.
- **Agent Loop**: the repeated process the Runner runs until a final answer.
- **RunResult**: object containing the run outputs (`final_output`, `new_items`, etc.).
- **RunResultStreaming**: a streaming run result that exposes events while the model produces output.
- **Session / SQLiteSession**: a conversation memory store so the agent can remember across runs.
- **ToolCallItem / ToolCallOutputItem**: items that show the model requested a tool and the tool's response.
- **Handoff**: an agent delegates work to another agent (specialist).
- **ModelSettings**: runtime knobs like `temperature` and `max_tokens`.

---

# 2 — The Agent Loop (plain step-by-step)

When you call the Runner to run an agent, the SDK does this automatically:

1. **Prepare input** — combine the agent’s `instructions` + session history (if any) + the new user message.
2. **Model step** — call the LLM. It returns either:
   - a **final output** (an answer), **or**
   - one or more **tool calls**, **or**
   - a **handoff** to another agent.
3. **Action step (optional)** — the Runner executes requested tool calls or performs the handoff, then appends those results to the conversation.
4. **Repeat** — the Runner sends the updated context back to the model and repeats steps 2–3 until the model produces `final_output` or the run exceeds safety limits (e.g., `max_turns`).

**Important rule:** If the model requests a tool or handoff, the Runner will run it and then loop again — you rarely write this orchestration yourself.

---

# 3 — Runner: the three simple run methods

### `Runner.run()` (async)

- What: the core async method that performs the agent loop and returns a `RunResult`.
- When: use inside async code (web servers, async notebooks).
- Example:

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name='A', instructions='Be brief.')
    result = await Runner.run(agent, 'Say hi')
    print(result.final_output)

asyncio.run(main())
```

---

### `Runner.run_sync()` (sync)

- What: a blocking convenience wrapper around `run()` that runs the async method under the hood.
- When: use in scripts, CLIs, and simple local tests — easiest for labs.
- Example:

```python
from agents import Agent, Runner

agent = Agent(name='A', instructions='Be brief.')
result = Runner.run_sync(agent, 'Say hello')
print(result.final_output)
```

---

### `Runner.run_streamed()` (streaming)

- What: runs the agent in streaming mode and yields events as the LLM produces them (token deltas, tool start/end). It returns a `RunResultStreaming` you can inspect when done.
- When: use for chat UIs or debugging when you want partial output immediately.
- Example (conceptual):

```python
from agents import Agent, Runner

agent = Agent(name='Streamer', instructions='Give two quick tips.')
with Runner.run_streamed(agent, 'Give two study tips for today.') as stream:
    for event in stream:
        print('EVENT:', type(event).__name__)
    final = stream.get_final_result()
print('Final:', final.final_output)
```

---

# 4 — RunResult: how to read what happened

After a run you get a `RunResult` (or `RunResultStreaming`). Inspect it in this order:

1. ``: the final human-facing answer (often a `str`). If present, the run ended with an answer.
2. ``: which agent produced the final answer (useful if handoffs happened).
3. ``: chronological list of items (messages, tool calls, tool outputs, handoffs, reasoning items).
4. ``: low-level model responses & metadata (tokens, model info) — helpful for debugging.
5. ``: convert the run + items into an input list you can pass into the Runner again (manual continuation without sessions).

**Quick inspect example**

```python
res = Runner.run_sync(agent, 'Explain recursion in 1 sentence')
print('final:', res.final_output)
print('last agent:', res.last_agent)
for item in res.new_items:
    print(type(item).__name__, getattr(item, 'raw_item', None))
# Manually continue if you want:
inputs = res.to_input_list()
inputs.append({'role': 'user', 'content': 'Expand the example.'})
res2 = Runner.run_sync(agent, inputs)
```

---

# 5 — Sessions: make the agent remember (easy)

**What sessions do:** they store run items so the agent remembers across separate `Runner.run()` calls.

**File-backed session example (recommended for production):**

```python
from agents import Agent, Runner, SQLiteSession

agent = Agent(name='MemoryAgent', instructions='Be brief and helpful.')
# Create or reuse a session that persists to disk:
session = SQLiteSession('user_123', 'day2_chat.db')

r1 = Runner.run_sync(agent, 'Hi there!', session=session)
print(r1.final_output)

r2 = Runner.run_sync(agent, 'What did I say earlier?', session=session)
print(r2.final_output)
```

**Session helper methods (common):**

- `session.get_items()` — list saved items.
- `session.pop_item()` — remove & return the last item (undo).
- `session.clear_session()` — wipe the session history.

**Use Cases:** chat apps, support bots, or any multi-turn flow where you want the agent to remember user data.

---

# 6 — Conversations & manual management

A single call to `Runner.run()` can involve multiple agents and many tool calls, but it represents one *logical turn* in a chat.

**Manual continuation (no sessions)**

- Use `res.to_input_list()` to convert a run into the SDK input format and append a new user message for the next run.

**Automatic management (Sessions)**

- Use `SQLiteSession` to automatically load previous items before each run and store new items after. This saves you from doing `to_input_list()` manually.

**Example: manual vs session**

```python
# Manual continuation (no sessions)
res = Runner.run_sync(agent, 'I like Python. Recommend a topic.')
inputs = res.to_input_list()
inputs.append({'role': 'user', 'content': 'Why that topic?'})
res2 = Runner.run_sync(agent, inputs)

# Using sessions (automatic)
session = SQLiteSession('my_chat')
res1 = Runner.run_sync(agent, 'Hi!', session=session)
res2 = Runner.run_sync(agent, 'What did I ask earlier?', session=session)
```

---

# 7 — Streaming (what it gives you)

Streaming sends intermediate events as the LLM produces output: partial text, tool-call starts/ends, and other events. At the end you still get the complete `RunResultStreaming` with full `new_items` and `final_output`.

When to use: UIs, progress indicators, or any student/developer experience where seeing partial results matters.

---

# 8 — Exceptions (plain language + tiny examples)

The SDK raises a few important exceptions. Handle them so your app stays stable.

- `` — base class for all SDK errors (catch for a general fallback).
- `` — the run exceeded the allowed number of loop turns (increase `max_turns` or simplify prompts).
- `` — the model produced invalid output (e.g., malformed JSON when a structured `output_type` was expected).
- `` — your code called the SDK incorrectly (wrong types or bad config).
- ``** / **`` — guardrails blocked the run due to safety or validation rules.

**Catch example**

```python
from agents import Agent, Runner
from agents.exceptions import MaxTurnsExceeded, AgentsException

agent = Agent(name='Loopy', instructions='Try to answer briefly.')
try:
    res = Runner.run_sync(agent, 'Do a long task', max_turns=2)
    print(res.final_output)
except MaxTurnsExceeded:
    print('Too many turns — simplify the task or raise max_turns.')
except AgentsException as e:
    print('Agent error:', type(e).__name__, str(e))
```

---

# 9 — Short, usable examples (copy & run)

### Example A — Async simple run

```python
# async_run.py
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name='Assistant', instructions='Answer concisely.')
    result = await Runner.run(agent, 'Write a haiku about recursion in programming.')
    print('Final:', result.final_output)

if __name__ == '__main__':
    asyncio.run(main())
```

### Example B — Sync run (scripts)

```python
# sync_run.py
from agents import Agent, Runner

agent = Agent(name='Assistant', instructions='Answer concisely.')
result = Runner.run_sync(agent, 'Explain recursion in one short sentence.')
print('Final:', result.final_output)
```

### Example C — Sessions example

```python
# session_sync.py
from agents import Agent, Runner, SQLiteSession

agent = Agent(name='Assistant', instructions='Reply briefly.')
session = SQLiteSession('conversation_123')

res1 = Runner.run_sync(agent, 'What city is the Golden Gate Bridge in?', session=session)
print('1:', res1.final_output)
res2 = Runner.run_sync(agent, 'What state is it in?', session=session)
print('2:', res2.final_output)
```

---

# 10 — Real-world scenario (short)

**Support triage**: user reports a billing problem → Triage agent identifies billing issue → handoff to Billing agent → Billing agent runs a DB lookup tool → Billing agent replies → session stores the conversation for follow-up.

This structure separates responsibilities, makes the system easier to debug, and keeps multi-turn context.

---

# 11 — Final notes (very short)

- Use `ModelSettings(temperature=0.0)` during development to make outputs predictable.
- Prefer a file-backed `SQLiteSession` for real apps so context survives restarts.
- Start with `Runner.run_sync()` for local testing; move to `run()` / `run_streamed()` when building servers or UIs.

---



T
﻿

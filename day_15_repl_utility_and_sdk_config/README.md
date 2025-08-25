# Day 15: REPL Utility and SDK Configuration

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

## Course Overview

Welcome to Day 15 of the OpenAI Agent SDK Mastery course.
This lesson wraps up Level 1 by introducing two practical developer tools that will become your daily companions when building agents:

REPL utility (run_demo_loop) – fast, interactive testing of agents directly in your terminal.



Together, they give you superpowers for fast iteration, debugging, and safe deployment.

Why This Matters

⚡ Faster iteration → Try prompts, tools, and instructions live instead of editing files + restarting.

🔍 Better debugging → Inspect RunResult, traces, tool calls, and outputs in real time.

🛡️ Safe experimentation → Test guardrails, sessions, and handoffs in a controlled terminal.



Real-World Scenarios Where REPL + Config Shine

Customer Support Bot → Use REPL to test handoffs between triage → billing → tech support.

Tutor App → Adjust temperature to balance creativity vs correctness when generating explanations.

Internal Tools → Safely test DB / code tools in REPL before wiring into web UI.

Prompt Engineering → Rapidly refine agent instructions interactively instead of guessing.

# 1. REPL Utility — run_demo_loop

The SDK provides run_demo_loop for quick, interactive testing of an agent’s behavior directly in your terminal.

Minimal Example

```python
import asyncio
from agents import Agent, run_demo_loop

async def main() -> None:
    agent = Agent(name="Assistant", instructions="You are a helpful assistant.")
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())
```

How It Works

Prompts for user input in a loop.

Remembers conversation history between turns.

Streams model output in real time (like a typewriter).

Exit by typing quit, exit, or pressing Ctrl-D.

When to Use REPL

Rapid prompt engineering & tuning.

Testing tools and function calls.

Debugging sessions / memory persistence.

Exploring traces & run configs live.

# 2. REPL Examples

## Advanced REPL with Tools, Sessions, and Traces

```python
import asyncio
from agents import Agent, Runner, SQLiteSession, function_tool, run_demo_loop, ModelSettings
from dotenv import load_dotenv
import os

load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("Please set OPENAI_API_KEY in your environment.")
    raise SystemExit(1)

# Tool
@function_tool
def add_numbers(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b

# Agent
agent = Agent(
    name="SmartChatBuddy",
    instructions="You’re a helpful assistant who uses tools for math and keeps answers short.",
    tools=[add_numbers],
)

async def main():
 
    await run_demo_loop(agent)

if __name__ == "__main__":
    asyncio.run(main())
```

# 3. CLI and Python REPL Usage

You can also use a plain Python REPL:

```python
from agents import Agent, Runner
agent = Agent(name="Helper", instructions="Answer concisely.")
Runner.run_sync(agent, "What is 2+2?")
```

Some SDKs also provide:

agents repl

But run_demo_loop is the canonical method.

# 4. Best Practices

🔑 Secrets → Store OPENAI_API_KEY in .env or secret manager.

💾 Persistent memory → use SQLiteSession("user", "sessions.db") to carry context across REPL restarts.

💸 Cost control → test with cheaper models first (e.g., gpt-3.5).

🌀 Prevent loops → set max_turns.

🧩 Guardrails → test input/output filtering inside REPL.

📦 Profiles → maintain dev/staging/prod configs for reproducibility.

# 5. Troubleshooting

REPL won’t start → pip install openai-agents, check Python 3.8+.

No streaming → confirm your terminal supports real-time output.

Session forgets → pass the same Session instance or SQLite db.

Tool ignored → ensure it has a clear @function_tool docstring.

Infinite loop → lower max_turns or refine agent instructions.

Trace empty → enable tracing, check trace_include_sensitive_data.

# 6. Security & Safety

Sensitive data → disable trace logging for private info.

Guardrails first → block malicious inputs early.

Tool safety → avoid giving REPL agents dangerous permissions.

# 7. Real-Life Examples

Startup Development → Test a support chatbot prototype in REPL before wiring into a web widget.

Healthcare AI → Validate medical assistant responses safely in REPL before exposing to patients.

Internal Productivity → Engineers use REPL to refine scheduling/email/report tools.

# 8. Why This is Powerful

Rapid Iteration → test ideas in seconds.

No Overhead → no need to build UIs during prototyping.

Context-Aware Testing → simulate real multi-turn conversations.

Real-Time Feedback → streaming makes it feel like a real chat.

# 9. Summary

The REPL utility (run_demo_loop) + SDK configuration together form your day-to-day toolkit for agent development.

Prototype faster.

Debug safer.

Deploy smarter.

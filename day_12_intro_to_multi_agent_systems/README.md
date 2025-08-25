# Day 12 — Multi‑Agent Systems (with Handoffs, Sessions, Tools & Tracing)

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

## Course Overview

Welcome to Day 12 of the **OpenAI Agent SDK Mastery** course! Yesterday you built a single‑agent Q&A app. Today we level up with **Multi‑Agent Systems (MAS)**—teams of specialized agents that collaborate via **handoffs**. This mirrors how real teams work: a planner decides, a researcher fetches info, a summarizer writes it up, a math specialist computes, etc. You’ll see how **handoffs**, **sessions** (memory), **tools**, and **tracing** combine to solve tasks more reliably.

---

## Why This Is Powerful

- **Specialization → Quality:** Each agent focuses on one responsibility (planner, researcher, summarizer, math, etc.), producing tighter, more accurate outputs.
- **Cost Control:** Route tasks to smaller/cheaper models where possible; reserve premium models only for the hard parts.
- **Scalability & Modularity:** Add/replace specialists without refactoring your entire app.
- **Robustness:** If one role struggles, others can take over or the planner can retry.
- **Closer to Real Workflows:** Mirrors human teams, making designs easier to reason about and maintain.

---

## What Is a Multi‑Agent System?

A **multi‑agent system** is a coordinated team of agents, each with a focused role and (optionally) its own tools. They collaborate by **passing control** with handoffs until the task is complete.

**Analogy:** A hospital team—triage → doctor → radiologist. Each professional (agent) handles the part they’re best at; the patient (task) flows through them.

---

## How It Works (Conceptual)

1. A **primary agent** (orchestrator/triage) receives the user’s request.
2. It decides to answer directly or **hand off** to a specialist.
3. Specialists may hand off again (e.g., research → summarize).
4. The final result flows back to the user.

The **Runner** executes this loop, **Sessions** persist memory across turns, and **Tracing** records the full workflow (inputs, tool calls, handoffs, outputs) for observability and debugging.

---

## Architecture at a Glance

- **Planner/Orchestrator:** Breaks down tasks; routes to specialists.
- **Specialists:** Narrow, focused instructions plus any needed tools (e.g., WebSearchTool, a math function, a code executor).
- **Handoffs:** The mechanism for passing control between agents.
- **Sessions:** Persist conversation context across turns and restarts (e.g., `SQLiteSession`).
- **Tracing:** Visualize end‑to‑end operations and decisions.

---

## Real‑World Examples

- **Customer Support:** A triage agent routes to billing, technical, or policy specialists; specialists may consult tools (order DB, knowledge base) and return the result.
- **Automated Research Pipeline:** A planner delegates to a researcher (web search + retrieval) and then to a summarizer (report paragraph or slide bullets).
- **Travel Planner:** Planner collects constraints, hands off to a booking agent to query APIs, then to an itinerary agent to format results.
- **Data ETL & Analysis:** Ingestion agent validates files, analyst agent runs calculations, reporter agent produces charts and an executive summary.
- **Software Development:** Code‑gen agent drafts, tester agent runs unit tests, fixer agent patches, doc agent explains the changes.
- **Compliance & Policy:** Classifier agent sorts requests, policy agent cites rules, redactor agent removes sensitive data.

---

## Real‑Life Examples (Everyday)

- **School Teachers:** You ask the main teacher, who hands math to the math teacher and history to the history teacher; you get one coherent answer back.
- **Hospital:** Nurse (intake) → GP (diagnosis) → Radiologist (imaging) → GP (plan). Each step is a specialized agent.
- **Startup Decisions:** Research agent pulls market data, analyst agent crunches numbers, planner agent recommends a go/no‑go strategy.
- **Homework Helper:** General tutor explains concepts; math tutor solves equations; writer tutor polishes final text.

---

## Setup

```bash
# Python 3.8+
python -m venv env
# macOS/Linux
source env/bin/activate
# Windows
# env\Scripts\activate

pip install openai-agents python-dotenv

# Required for OpenAI‑hosted models
export OPENAI_API_KEY="YOUR_KEY"

# Optional (only if you enable WebSearchTool in Example 2)
# export GOOGLE_API_KEY="..."
# export GOOGLE_CSE_ID="..."
```

> **Tip:** Wrap your runs in `with trace(workflow_name=..., group_id=...)` to label traces for easier debugging.

---

## Example 1 — Simple Triage: Generalist + Math Specialist (Handoff)

A general helper answers normal questions. If it detects math, it hands off to a math specialist.

```python
# simple_multi_agent.py
from agents import Agent, Runner

# Math specialist
math_agent = Agent(
    name="MathBuddy",
    handoff_description="Specialist for arithmetic and other math questions.",
    instructions=(
        "You are a math expert. Answer math questions clearly and briefly. "
        "Show only the essential steps if needed."
    ),
)

# General helper that can hand off to MathBuddy
general_agent = Agent(
    name="HelperBuddy",
    instructions=(
        "You are a friendly general assistant. "
        "If the user's query involves math or calculations, hand off to MathBuddy. "
        "Otherwise, answer directly and keep it concise."
    ),
    handoffs=[math_agent],
)

r1 = Runner.run_sync(general_agent, "What is a bird?")
print("General:", r1.final_output)

r2 = Runner.run_sync(general_agent, "What is 8 plus 5?")
print("Math:", r2.final_output)
```

**Expected output (sample):**

```
General: A bird is a feathered animal; many species can fly and lay eggs.
Math: 8 plus 5 is 13.
```

### Optional: Give MathBuddy a Tool

```python
from agents import function_tool

@function_tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two integers and return the product."""
    return a * b

math_agent = Agent(
    name="MathBuddy",
    handoff_description="Specialist for arithmetic and other math questions.",
    instructions="You are a math expert. Prefer using tools for calculations.",
    tools=[multiply_numbers],
)
```

---

## Example 2 — Orchestrated Pipeline: Planner → Researcher → Summarizer

The planner delegates research to a researcher (uses web search if available), then hands notes to a summarizer.

```python
# orchestrated_research_summary.py
import asyncio
from agents import Agent, Runner, SQLiteSession, trace,function_tool,WebSearchTool

# Optional WebSearchTool (only if available in your env)

# --- Specialists ---
# Researcher: uses web search when present; otherwise returns concise notes.
researcher = Agent(
    name="Researcher",
    handoff_description="Finds current, credible information from the web (or summarizes known info if web search is unavailable).",
    instructions=(
        "Collect relevant facts, stats, and sources about the user's topic. "
        "If WebSearchTool is available, use it. "
        "Return a short bullet list of key findings and any sources."
    ),
    tools=[WebSearchTool()],
)

# Summarizer: writes a concise paragraph from notes
summarizer = Agent(
    name="Summarizer",
    handoff_description="Turns research notes into a concise, well‑structured paragraph.",
    instructions=(
        "Write a single concise paragraph that synthesizes the Researcher's notes. "
        "Be factual, neutral, and readable for a general audience."
    ),
)

# Orchestrator/Planner
orchestrator = Agent(
    name="Planner",
    instructions=(
        "Coordinate specialists. For research tasks, first hand off to Researcher. "
        "Then hand off the notes to Summarizer to produce the final paragraph. "
        "Return the Summarizer's final paragraph to the user."
    ),
    handoffs=[researcher, summarizer],
)

async def main():
    session = SQLiteSession(user_id="day12_user", db_path="day12_multi_agent.db")

    with trace(workflow_name="Research & Summarize", group_id="day12"):
        query = "Research the history of AI and write a one‑paragraph summary."
        result = await Runner.run(orchestrator, query, session=session)
        print("\n--- Final Answer ---\n", result.final_output)

        # Follow‑up uses the same session (memory)
        followup = "Great. Add one concise source at the end."
        result2 = await Runner.run(orchestrator, followup, session=session)
        print("\n--- Follow‑up ---\n", result2.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

**What you’ll observe**

- The **Planner** first hands off to **Researcher**, then to **Summarizer**.
- **Tracing** shows the chain (Planner → Researcher → Summarizer).
- The **SQLiteSession** preserves context for follow‑ups (“Add one concise source…”).

> If your environment doesn’t have `WebSearchTool`, the Researcher still returns notes—just without fresh web hits.

---

## Optional — Streaming Handoffs Viewer (Minimal)

See which agent is active during handoffs while the answer forms.

```python
# stream_handoffs.py
import asyncio
from agents import Runner, SQLiteSession
from orchestrated_research_summary import orchestrator

async def main():
    session = SQLiteSession(user_id="stream_user", db_path="day12_stream.db")
    query = "Summarize the key milestones in AI from 1950 to 2010."

    stream = Runner.run_streamed(orchestrator, query, session=session)
    async for event in stream.stream_events():
        if event.type == "agent_updated_stream_event":
            print(f"[handoff] Active agent → {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            item = event.item
            if getattr(item, "type", "") == "message_output_item" and hasattr(item, "text"):
                print(item.text, end="", flush=True)

    final = await stream.get_final_result()
    print("\n\n--- Final ---\n", final.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Design Patterns & Tips

- **Write explicit instructions.** Tell the Planner _when_ to hand off and _to whom_. Tell specialists _how_ to format outputs.
- **Use **``**.** A short, specific tag helps routing (“Specialist for historical questions”).
- **Keep roles tight.** One purpose per agent (planner, researcher, summarizer, math…). Add more agents over time.
- **Memory via **``**.** Keep the same session for a conversation so follow‑ups

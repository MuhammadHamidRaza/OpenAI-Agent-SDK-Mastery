# Day 4 — Intro to Tools & Function Calling

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

## Course Overview

Welcome to **Day 4** of the *OpenAI Agent SDK Mastery* course! Today we unlock the most practical capability of agents: **Tools** and **Function Calling**. Tools let agents interact with the real world — call APIs, run calculators, query databases, manipulate files, and more. Function calling is the structured mechanism that connects the LLM’s reasoning to those tools.

This lesson is a single, polished guide with copy-paste examples, best practices, and real-world patterns so you know *exactly* when and how to use tools.

---

## TL;DR

* **Tools** are Python functions or built-in helpers you register with an agent so the agent can *act* (not just talk).
* Use the `@function_tool` helper to convert a Python function into a tool the agent can call.
* **Function calling** is the LLM generating a structured tool call (with arguments); the SDK executes the tool and returns the result back to the LLM.
* Register tools on `Agent(..., tools=[...])`. The agent decides when to call them.

---

## Objectives

By the end of Day 4 you will:

1. Understand what a tool is and why function calling matters.
2. Write and register function tools with the Agents SDK.
3. Run agents that call tools (sync and async examples).
4. Apply best practices and error handling for production-ready tools.

---

## 1) What is a Tool?

A **tool** is a function or capability you expose to your agent so it can perform actions beyond text generation. Examples:

* “get\_weather(city)” — fetch live weather.
* “add\_numbers(a, b)” — accurate math.
* “query\_employee(id)” — look up records in a database.

Tools make agents practical: they reduce hallucinations and let the agent rely on real, external data or deterministic computation.

---

## 2) Function Calling — the core idea

When a user asks something that requires external data (e.g., "What's the weather in Karachi?"), the LLM can decide to *call* a tool instead of directly answering. The LLM produces a structured function call (name + typed arguments). The SDK receives this call, runs the actual function/tool with those arguments, and feeds the tool result back to the LLM. The LLM then produces the final natural-language response.

**Conceptual flow:**

User → LLM (decides to call tool) → SDK executes tool → SDK provides tool output → LLM returns final reply.

---

## 3) How to create function tools (clean examples)

Use the `@function_tool` helper from the SDK. The decorator uses the function name, docstring, and Python type annotations to build a schema the model uses to call the tool.

### Example: simple calculator tool (math\_agent.py)

```python
# math_agent.py
from agents import Agent, Runner, function_tool

@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

# Create the agent and register the tool
agent = Agent(
    name="MathBuddy",
    instructions="You are a helpful assistant who uses tools to answer math questions.",
    tools=[add_numbers],
)

# Run synchronously (one-off script)
result = Runner.run_sync(agent, "What is 7 plus 5?")
print(result.final_output)
```

**What happens:** the agent recognizes the math question, generates a function call for `add_numbers`, the SDK runs your `add_numbers` tool, and the agent replies with the numerical result.

---

### Example: weather tool (weather\_agent.py) — mocked API

```python
# weather_agent.py
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Return a short, human-readable weather summary for the given city (mock)."""
    weather_db = {
        "London": "sunny, 20°C",
        "New York": "cloudy, 15°C",
        "Tokyo": "rainy, 18°C",
    }
    return weather_db.get(city, "I don't have weather data for that city.")

agent = Agent(
    name="WeatherBuddy",
    instructions="Use the get_weather tool for live weather queries.",
    tools=[get_weather],
)

async def main():
    result = await Runner.run(agent, "What's the weather in London?")
    print(result.final_output)

if __name__ == '__main__':
    asyncio.run(main())
```

**Note:** In production you would call a real weather API inside `get_weather()` and handle HTTP errors, timeouts and rate-limits.

---

## 4) Registering multiple tools & letting the agent choose

You can provide a list of tools; the LLM decides which to call based on the query.

```python
@function_tool
def multiply(x: int, y: int) -> int:
    return x * y

agent = Agent(name="Calc", instructions="Use tools for math.", tools=[add_numbers, multiply])
```

The agent will pick the correct tool (add vs multiply) using the tool metadata and argument schemas.

---

## 5) Best practices (do these!)

* **One job per tool:** single-purpose tools are easier for the LLM to choose.
* **Use clear docstrings:** the SDK uses the function docstring as tool description; write it for the model and future maintainers.
* **Type annotations:** annotate arguments and return types (the SDK uses them to build the tool schema and validate inputs/outputs).
* **Validate & sanitize inputs:** tools should defensively validate received arguments.
* **Graceful failure:** return informative errors or use `failure_error_function` (supported by the SDK) to provide structured error messages to the LLM.
* **Limit side-effects in dev:** when testing, prefer read-only or mocked tools to avoid unintended changes.
* **Small scope of permissions:** give tools only the permissions they need (e.g., DB read-only when appropriate).

---

## 6) Error handling & guardrails

* Use try/except inside tools to catch exceptions and return human-friendly messages.
* The SDK supports a `failure_error_function` for `@function_tool` to produce a controlled response when a function fails.
* Log raw responses (`result.raw_responses`) and guardrail results (`input_guardrail_results`, `output_guardrail_results`) for auditing.

Example pattern:

```python
@function_tool
def safe_fetch(id: str) -> str:
    try:
        # call external API or DB
        return "ok"
    except TimeoutError:
        return "error: timeout"
```

---

## 7) Real-world patterns & examples (when to use each)

* **Weather / Live Data Bots:** Use `get_weather`, `get_stock_price`, `web_search` tools to fetch fresh info. Use `Runner.run()` (async) if the operation is I/O-heavy.
* **Support Ticketing Agent:** Tool to create a ticket in your helpdesk (e.g., create\_ticket). Use `failure_error_function` to report ticket creation errors.
* **Finance & Currency Conversion:** Tools to query exchange rates or perform exact arithmetic.
* **Database Query Agent:** Tools that run parameterized SQL queries (use read-only credentials where possible).
* **Action Agents (automation):** Tools to schedule meetings, send emails, or perform CRUD actions — combine with guardrails and strict permissions.

---

## 8) Short exercises (practice)

1. Build `add_numbers` and `subtract_numbers` with `@function_tool`. Test prompts like "What's 150 - 45?".
2. Implement `get_weather` (mock) and add a city not in the dict — observe how the agent responds.
3. Create a failing tool that raises an exception and add `failure_error_function` to return a friendly message.

---

## 9) Quick checklist before you run code

* Python 3.8+ active venv.
* `pip install openai-agents python-dotenv`
* `OPENAI_API_KEY` in env or .env file.
* Use `@function_tool` to define tools and register them with `Agent(..., tools=[...])`.

---

## 10) Summary

Tools + function calling turn LLMs into *actors* — agents that can fetch live data, calculate precisely, and interact with systems. Use `@function_tool` to wrap Python functions, register them on your agent, and let the agent decide when to call them. Design tools carefully, validate inputs, and handle errors to build safe, reliable agentic apps.

---

*End of Day 4 — Tools & Function Calling (polished).*
Day 4 — Tools & Function Calling

Course Overview

Welcome to Day 4 of the OpenAI Agent SDK Mastery course! So far, you’ve learned what agents are (Day 1), how they make decisions (Day 2), and how they run (Day 3). Today, you make them super-powered using tools and function calling—the bridge between reasoning and real-world actions.

TL;DR

Tools are Python functions you register to empower agents (e.g., calculators, weather APIs).

Use the @function_tool decorator to wrap functions into tools that the agent can call.

The LLM suggests structured calls (tool + arguments); the SDK runs the actual function and returns the result.

This design makes agents practical, trustworthy, and powerful.

Objectives

By the end of Day 4, you’ll:

Understand what a tool is and how it's connected via function calling.

Write and register function tools with proper docstrings and type annotations.

Use agents that call tools (both sync and async).

Follow best practices and handle errors gracefully.

1) What Is a Tool?

A tool is a Python function (or helper) that the agent can use to act—beyond generating text.

Examples:

get_weather(city)

add_numbers(a, b)

query_database(id)

Tools let agents fetch live data, run accurate computations, or interact with external systems—making them practical and safe.

2) How Function Calling Works

Agent Reasoning: The LLM decides that a tool is needed and generates a structured call.

SDK Executes: Runs the actual function with provided arguments.

LLM Answers: The tool’s output is fed back to the agent to generate a natural response.

3) Writing Tools with @function_tool

Use the @function_tool decorator—leveraging function signatures and docstrings to auto-generate schemas.

Calculator Tool (Sync Example)
from agents import Agent, Runner, function_tool

@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

agent = Agent(
    name="MathBuddy",
    instructions="Use tools to answer math questions.",
    tools=[add_numbers]
)

result = Runner.run_sync(agent, "What is 7 plus 5?")
print(result.final_output)

Weather Tool (Async Example)
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Return mocked weather for a given city."""
    data = {"London": "sunny, 20 °C", "Tokyo": "rainy, 18 °C"}
    return data.get(city, "Unknown city")

agent = Agent(
    name="WeatherBuddy",
    instructions="Use the get_weather tool for weather questions.",
    tools=[get_weather]
)

async def main():
    result = await Runner.run(agent, "Weather in London?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

4) Advanced: Custom FunctionTool (When Not Using @function_tool)

If you need more control, you can create a FunctionTool by hand:

from agents import FunctionTool
from pydantic import BaseModel

class Args(BaseModel):
    username: str
    age: int

async def run_fn(ctx, args_json: str) -> str:
    args = Args.model_validate_json(args_json)
    return f"{args.username} is {args.age} years old."

tool = FunctionTool(
    name="process_user",
    description="Process user data.",
    params_json_schema=Args.model_json_schema(),
    on_invoke_tool=run_fn,
)


This method gives full control over schema and async behavior. 
OpenAI GitHub Pages

5) Best Practices

Single Responsibility: One purpose per tool.

Use Docstrings & Type Hints: Helps tools’ schema and clarity.

Validate & Sanitize: Guard against bad inputs.

Handle Errors Gracefully: Use failure_error_function or try/except.

Scope & Permissions: Limit side effects and permissions.

6) Real-World Patterns

Live data bots—weather, stock prices, news via APIs.

Automation agents—create tickets, schedule tasks via tools.

Interactive UIs—tools for UI events like file upload, commands.

Security-aware tools—tools gated by guardrails or approval flows.

7) Quick Exercise

Create subtract_numbers as a tool; ask subtraction prompts.

Extend the weather tool with more cities or real API calls.

Build a failing tool and use failure_error_function to return friendly errors.

8) Summary

Tools make agents act, not just talk.

@function_tool provides auto-generated schemas—simple and powerful.

The agent decides when to call tools using LLM reasoning, then the SDK executes the function.

Write clean, documented tools and handle errors for safety & clarity.

Would you like me to:

Translate this Day 4 lesson into Urdu?

Combine Days 1–4 into a downloadable PDF or slide deck?

Add a real-world async example (e.g., a FastAPI endpoint that uses a tool)?

Let me know and I’ll take it from there!

Handling errors in function tools
When you create a function tool via @function_tool, you can pass a failure_error_function. This is a function that provides an error response to the LLM in case the tool call crashes.

By default (i.e. if you don't pass anything), it runs a default_tool_error_function which tells the LLM an error occurred.
If you pass your own error function, it runs that instead, and sends the response to the LLM.
If you explicitly pass None, then any tool call errors will be re-raised for you to handle. This could be a ModelBehaviorError if the model produced invalid JSON, or a UserError if your code crashed, etc.

from agents import function_tool, RunContextWrapper
from typing import Any

def my_custom_error_function(context: RunContextWrapper[Any], error: Exception) -> str:
    """A custom function to provide a user-friendly error message."""
    print(f"A tool call failed with the following error: {error}")
    return "An internal server error occurred. Please try again later."

@function_tool(failure_error_function=my_custom_error_function)
def get_user_profile(user_id: str) -> str:
    """Fetches a user profile from a mock API.
     This function demonstrates a 'flaky' or failing API call.
    """
    if user_id == "user_123":
        return "User profile for user_123 successfully retrieved."
    else:
        raise ValueError(f"Could not retrieve profile for user_id: {user_id}. API returned an error.")
If you are manually creating a FunctionTool object, then you must handle errors inside the on_invoke_tool function.
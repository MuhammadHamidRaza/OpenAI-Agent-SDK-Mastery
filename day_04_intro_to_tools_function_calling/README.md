# Day 4: Intro to Tools & Function Calling

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 4 of the **OpenAI Agent SDK Mastery** course! So far, we've established what AI agents are and how to execute them using the `Runner`. Today, we introduce a critical concept that unlocks the true power of agents: **Tools** and **Function Calling**. While Large Language Models (LLMs) are incredibly powerful for understanding and generating text, they are inherently limited to the data they were trained on. Tools provide a mechanism for agents to interact with the external world, access real-time information, perform calculations, or trigger actions. You'll learn why tools are indispensable for building practical, real-world agentic applications.

---

## The Limitations of LLMs Alone

Large Language Models (LLMs) are remarkable for their ability to process and generate human-like text. They excel at tasks like:

*   **Text Generation:** Writing articles, emails, creative content.
*   **Summarization:** Condensing long documents into key points.
*   **Translation:** Converting text from one language to another.
*   **Question Answering (based on training data):** Answering factual questions if the information was part of their training corpus.

However, LLMs have inherent limitations:

*   **Lack of Real-time Information:** Their knowledge is static, based on their last training cut-off. They cannot access current events, live data, or dynamic information from the internet.
*   **Inability to Perform Actions:** LLMs cannot directly interact with external systems, execute code, send emails, or query databases.
*   **Mathematical Inaccuracies:** While they can generate text about math, they are not reliable calculators and can make errors in precise computations.
*   **Hallucinations:** They can sometimes generate plausible-sounding but incorrect or fabricated information.

This is where **Tools** come into play.

---

## Why Agents Need Tools

Tools are external functionalities that an agent can invoke to overcome the limitations of the LLM. They extend the agent's capabilities, allowing it to:

*   **Access Up-to-date Information:** A web search tool can provide current news, weather, or stock prices.
*   **Perform Complex Calculations:** A calculator tool can ensure accurate mathematical operations.
*   **Interact with External Systems:** Tools can be built to query databases, send API requests, manage files, or control IoT devices.
*   **Execute Code:** A code interpreter tool allows the agent to write and run code, useful for data analysis or complex logic.

Think of an agent as a highly intelligent person. Without tools, they can only use their brain. With tools (like a computer, a phone, a calculator, or a car), they can achieve much more in the real world.

---

## Introduction to Function Calling

**Function Calling** is the mechanism by which an LLM (the brain of our agent) decides which tool to use and how to use it. It's a powerful capability that allows the LLM to:

1.  **Understand Intent:** Analyze the user's request and determine if an external action (tool use) is required.
2.  **Select Tool:** Identify the most appropriate tool from a predefined set of available tools.
3.  **Extract Arguments:** Determine the necessary arguments or parameters to pass to the selected tool based on the user's input.
4.  **Format Call:** Generate a structured call (often in JSON format) that represents the invocation of the tool with its arguments.

When an LLM performs function calling, it doesn't *execute* the tool itself. Instead, it *suggests* or *describes* the tool call. The Agent SDK (or your application logic) then intercepts this suggestion, executes the actual tool, and feeds the tool's output back to the LLM. This creates a powerful loop:

**User Request -> LLM (decides tool) -> Tool Execution -> Tool Output -> LLM (processes output) -> Final Response**

### How it Works (Conceptual Flow):

1.  **Tool Definition:** You define tools with clear descriptions of what they do and what parameters they accept. This metadata is provided to the LLM.
2.  **User Query:** A user asks a question or gives a command (e.g., "What's the weather like in London?").
3.  **LLM Reasoning:** The LLM, aware of the available tools, analyzes the query. It recognizes that to answer the weather question, it needs a "weather tool" and that "London" is the location parameter.
4.  **Function Call Generation:** The LLM generates a structured output (e.g., `call_weather_tool(location="London")`).
5.  **SDK Interception:** The Agent SDK intercepts this generated function call, not as a direct answer, but as an instruction to perform an action.
6.  **Tool Execution:** The SDK executes the actual `weather_tool` with `location="London"`.
7.  **Tool Output:** The `weather_tool` returns the current weather in London (e.g., "It's 15°C and cloudy.").
8.  **LLM Re-processing:** The SDK feeds this tool output back to the LLM.
9.  **Final Response:** The LLM processes the tool's output and generates a natural language response to the user (e.g., "The weather in London is currently 15 degrees Celsius and cloudy.").

This iterative process allows agents to perform complex, multi-step tasks that go far beyond simple text generation.

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
```

---

## 7) Real-world patterns & examples (when to use each)

* **Weather / Live Data Bots:** Use `get_weather`, `get_stock_price`, `web_search` tools to fetch fresh info. Use `Runner.run()` (async) if the operation is I/O-heavy.
* **Support Ticketing Agent:** Tool to create a ticket in your helpdesk (e.g., create_ticket). Use `failure_error_function` to report ticket creation errors.
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
# Day 5: Defining Python Functions as Tools

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 5 of the **OpenAI Agent SDK Mastery** course! Yesterday, we introduced the crucial concept of tools and function calling, understanding *why* agents need to interact with the external world. Today, we'll get hands-on and learn *how* to transform your ordinary Python functions into powerful tools that your agents can leverage. The OpenAI Agents SDK makes this process incredibly straightforward, primarily through the use of the `@function_tool` decorator. By the end of this session, you'll be able to define custom tools that extend your agent's capabilities far beyond simple text generation.

---

## The `@function_tool` Decorator: Your Gateway to Agent Capabilities

At the heart of defining tools in the OpenAI Agents SDK is the `@function_tool` decorator. This decorator allows you to register any standard Python function as a tool that your agent can discover and use. When you decorate a function with `@function_tool`, the SDK automatically generates the necessary metadata (like the function's name, description, and parameters) that the underlying Large Language Model (LLM) uses for function calling.

### How it Works:

1.  **Import:** You import the `function_tool` decorator from the `agents.tools` module.
2.  **Decorate:** You place `@function_tool` directly above your Python function definition.
3.  **Docstrings are Key:** The docstring of your function becomes the `description` that the LLM sees. A clear and concise docstring is crucial for the LLM to understand when and how to use your tool.
4.  **Type Hints for Parameters:** Use standard Python type hints for your function's parameters. These type hints are used by the SDK to inform the LLM about the expected types of arguments for the tool.

Let's look at some examples.

---

## Example 1: A Simple Calculator Tool

This tool will perform basic addition. Notice how the docstring clearly explains its purpose and parameters.

```python
from agents import Agent, Runner
from agents.tools import function_tool
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

@function_tool
def add_numbers(a: float, b: float) -> float:
    """Adds two numbers together and returns the sum.

    Args:
        a: The first number.
        b: The second number.

    Returns:
        The sum of the two numbers.
    """
    return a + b

# Define an agent that can use the add_numbers tool
agent = Agent(
    name="CalculatorAgent",
    instructions="You are a helpful assistant that can perform basic arithmetic operations.",
    tools=[add_numbers] # We will cover passing tools to agents in detail tomorrow
)

# Example of how the agent might use this tool (conceptual for now)
# In a real scenario, the agent would decide to call this based on user input
# result = Runner.run_sync(agent, "What is 15 + 27?")
# print(result.final_output)

print("Tool 'add_numbers' defined successfully. Ready for agent integration.")

```

**Explanation:**

*   The `add_numbers` function is decorated with `@function_tool`.
*   Its docstring provides a clear description, which the LLM uses to understand the tool's functionality.
*   Type hints (`a: float`, `b: float`, `-> float`) inform the SDK (and thus the LLM) about the expected input and output types.

---

## Example 2: A Simple Greeting Tool

This tool will generate a personalized greeting.

```python
from agents import Agent, Runner
from agents.tools import function_tool
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

@function_tool
def greet_user(name: str) -> str:
    """Generates a personalized greeting for a user.

    Args:
        name: The name of the user to greet.

    Returns:
        A personalized greeting string.
    """
    return f"Hello, {name}! Nice to meet you."

# Define an agent that can use the greet_user tool
agent = Agent(
    name="GreeterAgent",
    instructions="You are a friendly assistant that can greet people by name.",
    tools=[greet_user] # We will cover passing tools to agents in detail tomorrow
)

# Example of how the agent might use this tool (conceptual for now)
# result = Runner.run_sync(agent, "Say hello to Alice.")
# print(result.final_output)

print("Tool 'greet_user' defined successfully. Ready for agent integration.")

```

**Explanation:**

*   Similar to the previous example, `@function_tool` registers `greet_user`.
*   The docstring and type hint (`name: str`) guide the LLM on how to use this tool for generating greetings.

---

## Key Considerations for Defining Tools

*   **Clear Docstrings:** This is paramount. The LLM relies heavily on the docstring to understand the tool's purpose, arguments, and return values. Be precise and descriptive.
*   **Accurate Type Hints:** Use standard Python type hints (`str`, `int`, `float`, `bool`, `list`, `dict`, `Optional`, `Union`, etc.) to define the expected types for inputs and outputs. This helps the LLM construct correct function calls.
*   **Atomic Functions:** Ideally, each tool should perform a single, well-defined task. This makes it easier for the LLM to decide when to use a tool and reduces complexity.
*   **Error Handling:** While not explicitly shown in these simple examples, real-world tools should include robust error handling to gracefully manage unexpected inputs or external system failures.
*   **No Side Effects (Preferably):** For predictability, tools that primarily return information are often preferred. If a tool has side effects (e.g., modifying a database), ensure its description clearly states this.

---

## What's Next?

Today, you've learned the fundamental skill of defining custom tools using `@function_tool`. Tomorrow, on Day 6, we will take the next crucial step: **integrating these tools with your agents** and observing how the agent dynamically selects and uses them to fulfill user requests. Get ready to see your agents become even more capable!
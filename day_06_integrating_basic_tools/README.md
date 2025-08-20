# Day 6: Integrating Basic Tools

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 6 of the **OpenAI Agent SDK Mastery** course! Yesterday, you mastered the art of defining custom tools using the `@function_tool` decorator. Today, we bridge the gap between defining tools and making your agents truly intelligent: we'll learn how to **integrate these tools directly into your agents**. This is where the magic of function calling comes alive, as you'll observe your agent dynamically selecting and utilizing the appropriate tools to fulfill user requests. By the end of this session, your agents will be able to perform actions in the real world, moving beyond mere text generation.

---

## How to Integrate Tools with an Agent

Integrating tools with an agent in the OpenAI Agents SDK is straightforward. When you instantiate an `Agent` object, you can pass a list of your defined tools to its `tools` parameter. The SDK then makes these tools available to the underlying Large Language Model (LLM).

When the agent receives a prompt, the LLM will:

1.  **Analyze the Request:** Understand the user's intent.
2.  **Consult Available Tools:** Review the descriptions and parameters of all tools provided to it.
3.  **Decide on Tool Use:** Determine if any of the tools can help fulfill the request.
4.  **Generate Function Call:** If a tool is needed, it will generate a structured function call (as we discussed on Day 4).
5.  **Execute Tool:** The `Runner` (which we covered on Day 3) will then execute the actual Python function associated with the tool.
6.  **Process Output:** The output from the tool is fed back to the LLM, which then formulates a coherent response to the user.

Let's integrate the `add_numbers` and `greet_user` tools we defined yesterday into an agent.

---

## Example 1: Agent Using the `add_numbers` Tool

We'll create an agent that can perform addition using the `add_numbers` tool.

```python
from agents import Agent, Runner
from agents.tools import function_tool
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define the add_numbers tool (from Day 5)
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

# Define the Agent and pass the tool to it
calculator_agent = Agent(
    name="CalculatorAgent",
    instructions="You are a helpful assistant that can perform arithmetic operations. Use the provided tools to calculate sums.",
    tools=[add_numbers] # <--- Here we pass the tool to the agent
)

# Run the agent with a prompt that requires the tool
print("Running CalculatorAgent...")
result = Runner.run_sync(calculator_agent, "What is 123.45 + 67.89?")

# Print the final output from the agent
print("Agent's response:", result.final_output)

# Another example
print("\nRunning CalculatorAgent with another sum...")
result2 = Runner.run_sync(calculator_agent, "Can you tell me the sum of 500 and 750?")
print("Agent's response:", result2.final_output)

```

**Expected Behavior:**

When you run this code, the `CalculatorAgent` will receive the prompt. The LLM will recognize that the request involves addition and that the `add_numbers` tool is available. It will then generate a function call to `add_numbers` with the appropriate arguments. The SDK executes this function, and its result is fed back to the LLM, which then formulates the final answer.

---

## Example 2: Agent Using the `greet_user` Tool

Now, let's integrate the `greet_user` tool.

```python
from agents import Agent, Runner
from agents.tools import function_tool
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define the greet_user tool (from Day 5)
@function_tool
def greet_user(name: str) -> str:
    """Generates a personalized greeting for a user.

    Args:
        name: The name of the user to greet.

    Returns:
        A personalized greeting string.
    """
    return f"Hello, {name}! Nice to meet you."

# Define the Agent and pass the tool to it
greeter_agent = Agent(
    name="GreeterAgent",
    instructions="You are a friendly assistant that can greet people by name using the provided tool.",
    tools=[greet_user] # <--- Here we pass the tool to the agent
)

# Run the agent with a prompt that requires the tool
print("\nRunning GreeterAgent...")
result = Runner.run_sync(greeter_agent, "Please greet John Doe.")

# Print the final output from the agent
print("Agent's response:", result.final_output)

# Another example
print("\nRunning GreeterAgent with another name...")
result2 = Runner.run_sync(greeter_agent, "Say hello to Alice.")
print("Agent's response:", result2.final_output)

```

**Expected Behavior:**

Similar to the `CalculatorAgent`, the `GreeterAgent` will use the `greet_user` tool when prompted to greet someone. The LLM will extract the name from the prompt and pass it as an argument to the tool.

---

## Key Takeaways

*   Tools are integrated with an agent by passing a list of `@function_tool` decorated functions to the `tools` parameter of the `Agent` constructor.
*   The agent's underlying LLM intelligently decides when to use a tool based on its instructions and the user's prompt.
*   The SDK handles the entire function calling lifecycle: from the LLM suggesting a tool call, to executing the Python function, and feeding the output back to the LLM.
*   By integrating tools, your agents gain the ability to perform real-world actions and access dynamic information, significantly expanding their utility.

---

## Summary

Tools + function calling turn LLMs into *actors* — agents that can fetch live data, calculate precisely, and interact with systems. Use `@function_tool` to wrap Python functions, register them on your agent, and let the agent decide when to call them. Design tools carefully, validate inputs, and handle errors to build safe, reliable agentic apps.

---

Today, you've made your agents truly interactive by giving them the ability to use custom tools. Tomorrow, we'll explore how to leverage powerful, pre-built tools like web search and file search to give your agents access to vast amounts of information.

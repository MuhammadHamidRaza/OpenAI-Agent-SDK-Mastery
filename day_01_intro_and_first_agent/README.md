
# Day 1: Intro to AI Agents & Your First Agent!

### **Course Overview**

Welcome to Day 1 of the **OpenAI Agent SDK Mastery** course! Today, we're setting the stage for our 45-day journey. We'll start with the foundational concepts of agentic AI and then use the SDK to create and run your very first agent.

## What is an AI Agent?

An AI agent is more than just a large language model (LLM). It’s an intelligent system that goes beyond just answering questions. It's an entity that can take actions, solve problems, and achieve goals. An agent is a combination of:

-   **Perceive/Perception**: Take in information from the world, like a user's question or the result of a tool.
    
-   **Reason/Reasoning**: Think about the information and decide on the best course of action.
    
-   **Act/Action**: Perform an action, which could be giving a final answer, running a tool, or delegating a task. Think of an LLM as the brain, while the agent is the full body, equipped with senses (tools) and the ability to act on the world. This is what makes agents so powerful for building real-world applications.
    

## Analogy for a 5-Year-Old

Imagine you're in a big school with many teachers.

-   🧑‍🏫 The Math Teacher helps with math problems.
    
-   🧑‍🏫 The History Teacher helps with history questions.
    
-   🧑‍🏫 The Receptionist decides who the student should talk to. This is how the Agents SDK works:
    
-   The student (user) asks a question.
    
-   The receptionist agent reads the question and hands it off to the right teacher (agent).
    
-   The teacher may use a tool like a calculator.
    
-   If the question is naughty, a guardrail might block it before it even reaches the teacher.
    
-   Everything is recorded nicely so you can see what happened and debug it (called tracing).
    

## What is the OpenAI Agents SDK?

The OpenAI Agents SDK is a lightweight, Python-first framework that simplifies the process of building these powerful agents. It provides a built-in agent loop that handles the core logic for you, allowing you to focus on the instructions and tools that make your agent smart. It’s an easy-to-learn, yet production-ready tool. It's a production-ready upgrade of previous work, meaning it's reliable for real-world projects.

The SDK is built around a few core ideas, which are called **Primitives**. These simplify complex tasks:

-   **Agents**: These are AI brains (LLMs) that have been given specific instructions and tools to do a job.
    
-   **Handoffs**: This is a powerful feature that lets one agent pass a task to another agent who is an expert in that area. It's like delegating work to a specialist on your team.
    
-   **Guardrails**: These are like safety checks. They automatically validate the information that goes into and comes out of your agent, ensuring everything stays within safe and defined rules.
    
-   **Sessions**: This automatically handles the conversation history. Your agent will remember past questions and answers without you needing to write extra code. By combining these simple ideas with Python, you can build complex and useful applications without a steep learning curve. The SDK also has a built-in tracing feature that lets you see exactly how your agent is "thinking," which is great for debugging and making improvements.
    

## Why Use It?

The SDK was designed to be both powerful and simple. Here are its main features, explained in easy terms:

-   **Easy with Python**: The SDK works naturally with Python. You can use standard Python functions to build your agents, so there's no need to learn a whole new language or complex rules.
    
-   **Real-World Workflows**: It allows you to build sophisticated, multi-step AI applications for practical use cases.
    
-   **Built-in Primitives**: It comes with native support for tools, agents, handoffs, and guardrails, simplifying complex orchestration.
    
-   **Visibility**: The built-in tracing helps you visualize and debug what happened during the AI's "thinking" process. It also helps you fine-tune your models, which means making the AI better at your specific task.
    
-   **Agent Loop**: This is the built-in system that makes the agent run. It handles calling tools and figuring out what to do next, so you don't have to.
    
-   **Sessions**: This is the automatic memory management that keeps track of the conversation, making your agent feel more like a smart conversational partner.
    
-   **Function Tools**: You can turn any Python function into a tool for your agent, and the SDK automatically understands how to use it.
    

## Getting Started: Installation & Setup

To begin, you need to install the SDK. Open your terminal or command prompt and run the following command:

```python
pip install openai-agents

```

You also need an OpenAI API key. Make sure you set it as an environment variable so your code can access it securely.

```python
export OPENAI_API_KEY="your-api-key-here"

```

## Your First Agent: "Hello World" Example

Now, let's create a simple Python file (e.g., `main.py`) and write the code for our first agent. This agent will have a simple instruction: to be a helpful assistant that writes haikus about programming concepts.

```python
from agents import Agent, Runner
import os

# Ensure the OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# 1. Define the Agent with a name and instructions.
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. You are an expert at writing haikus about programming concepts."
)

# 2. Use the Runner to run the agent with a prompt.
result = Runner.run_sync(
    agent,
    "Write a haiku about recursion in programming."
)

# 3. Print the final output from the agent.
print(result.final_output)

```

### Expected Output:

```
Code within the code,
Functions calling themselves now,
Infinite loop’s dance.

```

### How It Works:

-   **Agent**: We create an instance of the Agent class, providing a name and a set of instructions. These instructions act as the system prompt, defining the agent's purpose and personality.
    
-   **Runner**: The Runner class is responsible for executing the agent. We use `run_sync()` for a simple, synchronous execution.
    
-   **result.final_output**: The output is contained within a `RunResult` object. We access the final, human-readable response through the `.final_output` attribute.
# OpenAI Agent SDK Mastery: Course Overview & Detailed Curriculum

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](./LICENSE)

---

### **Part 1: The Foundational Layer & Course Overview**

The **OpenAI Agents SDK** enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. This course, **OpenAI Agent SDK Mastery**, is designed as a project-based guide to help you build powerful, autonomous AI systems.

#### **Core Concepts: The Power of Simplicity in Design**

What truly sets the Agents SDK apart is its thoughtful balance of simplicity and power. The SDK is built around a small set of core primitives that our course will explore in depth:

* **Agents:** These are language models (LLMs) configured with specific instructions and tools. Our course will teach you to build specialized agents for different tasks.
* **Handoffs:** A powerful feature that allows one agent to delegate tasks to another specialized agent. You'll learn how to build complex, coordinated workflows with ease.
* **Guardrails:** Built-in safety checks that validate inputs and outputs, ensuring your agents operate within defined parameters and minimizing risks.
* **Sessions:** This primitive automatically maintains a conversation's history across agent runs, freeing you from manual state handling.
* **Tracing & Observability:** The SDK includes integrated tracing capabilities that allow you to visualize and debug the flow of an agent’s actions, which is a key part of our curriculum.

This minimalist approach makes the SDK approachable for newcomers while providing enough flexibility for experienced developers to build sophisticated systems.

#### **Why This Course Matters**

By abstracting much of the orchestration logic that was previously handled manually, the Agents SDK simplifies the development process, allowing you to focus on building the core functionalities of your application. With fewer abstractions and a Python-centric approach, it’s easier to maintain, extend, and debug complex agent workflows. Our **45-day masterclass** is designed to take you from a beginner to an expert in this field.

---

### **Part 2: The 45-Day Detailed Curriculum**

This section outlines every class in our masterclass. Each day corresponds to a dedicated folder in this repository, containing all the code and materials you need to follow along.

#### **Level 1: Agent Fundamentals & Your First Project (Days 1-15)**

This foundational level introduces the core concepts and the fundamental building blocks of the SDK.

* **Day 1: Intro to AI Agents & Your First Agent!**
    * Learn the basics of agentic AI and run your very first "Hello World" agent.
* **Day 2: Deconstructing the Agent Loop & Sessions**
    * A deep dive into how the agent processes requests and how `Sessions` manage conversation history.
* **Day 3: Understanding `Runner` and Basic Execution**
    * Explore the `Runner` class and its methods (`run_sync`, `run_streamed`) for executing agents.
* **Day 4: Intro to Tools & Function Calling**
    * Understand why agents need tools and the concept of function calling for external interactions.
* **Day 5: Defining Python Functions as Tools**
    * Learn to convert any Python function into a powerful agent tool using the `@function_tool` decorator.
* **Day 6: Integrating Basic Tools**
    * Pass tools to your agent and observe how it dynamically selects and uses them.
* **Day 7: Hosted Tools: Web Search**
    * Leverage built-in tools like `WebSearchTool` to give your agent access to real-time information.
* **Day 8: Intro to Agent Memory**
    * Learn the importance of memory for conversational continuity and the distinction between short-term and long-term memory.
* **Day 9: `RunResult` and Streaming**
    * Understand the detailed `RunResult` object and implement streaming output for a better user experience.
* **Day 10: `Tracing` for Observability**
    * Learn to visualize and debug your agent's workflow using the SDK's powerful built-in tracing.
* **Day 11: **Project 1: Simple Q&A Agent****
    * Build a complete Q&A agent by synthesizing your knowledge of sessions, tools, and tracing.
* **Day 12: Intro to Multi-Agent Systems**
    * Understand the rationale behind using a team of agents for complex tasks.
* **Day 13: Intro to `Handoffs`**
    * Learn the foundational concept of `Handoffs` for delegating tasks between agents.
* **Day 14: Intro to `Guardrails`**
    * Understand the purpose of `Guardrails` in ensuring agent safety and reliability.
* **Day 15: `REPL Utility` and SDK Configuration**
    * Use the `REPL` utility for interactive development and configure SDK settings.

#### **Level 2: Intermediate Development & Projects (Days 16-30)**

This level covers advanced tool integrations, multi-agent coordination, and essential security measures.

* **Day 16: Code Interpreter Tool**
    * Learn to use the `CodeInterpreterTool` to give your agent the ability to execute Python code.
* **Day 17: Custom Tool Development & API Integration**
    * Build custom tools that interface with external APIs for more powerful applications.
* **Day 18: Implementing `Handoffs`**
    * Create a practical scenario where one agent hands off a task to a specialized agent.
* **Day 19: Orchestrating Multi-Agent Workflows**
    * Design and manage complex workflows where multiple agents collaborate.
* **Day 20: Agent Planning**
    * Explore how an agent can autonomously plan a sequence of actions to solve a problem.
* **Day 21: `ReAct` Pattern: Reasoning and Acting**
    * Deep dive into the `ReAct` pattern, where agents cycle through thought, action, and observation.
* **Day 22: **Project 2: Automated Research Assistant****
    * Build a multi-agent research system that uses a team of agents to find information and generate a report.
* **Day 23: Agent Reflection & Self-Correction**
    * Implement internal feedback loops that allow an agent to evaluate its own work and correct its path.
* **Day 24: Input & Output Validation Guardrails**
    * Apply practical `Guardrails` to validate and filter agent inputs and outputs.
* **Day 25: Mitigating Prompt Injection Attacks**
    * Learn how to identify and prevent prompt injection attacks, a key security concern.
* **Day 26: `Realtime` Agents Intro**
    * Understand the foundational concepts of `Realtime` agents for low-latency applications.
* **Day 27: `Voice` Agents Intro**
    * Learn the basics of `Voice` agents, including Speech-to-Text and Text-to-Speech.
* **Day 28: Long-Term Memory Intro**
    * Explore the necessity of persistent, long-term memory that goes beyond a single session.
* **Day 29: Vector Stores and RAG**
    * Implement Retrieval-Augmented Generation (RAG) by connecting your agent to a vector store.
* **Day 30: Advanced Memory Optimization**
    * Learn advanced techniques to optimize your agent's memory usage and management.

#### **Level 3: Advanced Topics & Final Projects (Days 31-45)**

This final level focuses on optimizing agents for production, exploring voice capabilities, and building your most ambitious projects.

* **Day 31: **Project 3: Voice-Enabled Task Manager****
    * Build a complete agent that handles tasks and calendar entries using voice commands.
* **Day 32: Model Routing and Selection**
    * Create an intelligent system that automatically routes queries to the most appropriate LLM.
* **Day 33: Caching Strategies**
    * Implement caching to reduce latency and lower costs for frequently accessed queries.
* **Day 34: Agent Visualization**
    * Use the SDK's tools to generate visual representations of your agent’s workflow.
* **Day 35: SDK Configuration & `RunConfig`**
    * Master the `RunConfig` object to customize the behavior of individual agent runs.
* **Day 36: `Realtime` Agents Implementation**
    * Build a low-latency agent from scratch, perfect for live chat scenarios.
* **Day 37: `Voice` Agents Implementation**
    * Implement a fully functional voice-enabled agent that can listen and speak with users.
* **Day 38: **Project 4: Real-time Stock Analyst****
    * Build an agent that analyzes real-time stock data and provides insights based on current events.
* **Day 39: Advanced Multi-Agent Patterns**
    * Explore complex patterns like a supervisor agent and human-in-the-loop workflows.
* **Day 40: Evaluating Agent Performance & Fine-Tuning**
    * Learn to define metrics for agent performance and the process of fine-tuning models.
* **Day 41: Production Best Practices**
    * A comprehensive overview of best practices for deploying agents at scale.
* **Day 42: Release Process & Changelog**
    * Understand the importance of version control and maintaining a clear changelog for your projects.
* **Day 43: API Reference & Extensions**
    * Learn how to effectively navigate the SDK's API reference and explore powerful extensions.
* **Day 44: **Project 5: Ultimate Personal Assistant****
    * This is your final project: build an all-in-one assistant that integrates voice, real-time data, and a multi-agent system.
* **Day 45: Final Thoughts & Course Conclusion**
    * A comprehensive review of your entire journey and a look at the future of AI agents.


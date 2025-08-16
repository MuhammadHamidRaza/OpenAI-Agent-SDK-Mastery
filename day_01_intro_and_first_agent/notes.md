# Day 1: Intro to AI Agents & Your First Gemini Agent

## 1. Key Concepts

- **AI Agent**: An autonomous system that can:
  - Perceive (take input)
  - Reason (decide what to do)
  - Act (perform an action or call a tool)

- **LLM vs Agent**:
  - LLM = Brain
  - Agent = Brain + Body + Senses (tools)

- **OpenAI Agents SDK Primitives**:
  - **Agents**: AI brains with instructions & tools.
  - **Handoffs**: Delegate tasks to specialized agents.
  - **Guardrails**: Safety & input/output validation.
  - **Sessions**: Automatic conversation history.
  - **Tracing**: Visualize agent actions.

## 2. Gemini Agent Setup

- **API Key**: Stored in `.env` file as `GEMINI_API_KEY`.
- **AsyncOpenAI client**: Connects to Gemini endpoint.
- **OpenAIChatCompletionsModel**: Wraps Gemini model for Agents SDK.
- **Agent**: Defined with name and model.
- **Runner.run_sync**: Executes agent and retrieves `final_output`.

## 3. First Task

**Prompt:** `"Write a haiku about recursion in programming."`  
**Expected Output:**
```
Code within the code,
Functions calling themselves now,
Infinite loop’s dance.
```

## 4. Notes / Tips

- Always load API key from `.env` to avoid exposing it.
- Use `run_sync` for simple scripts; `run` (async) for notebooks/web apps.
- Keep instructions simple for the first agent; complexity comes later.
- Observe how agent responds with no tools—this shows base reasoning.

## 5. Homework / Practice

- Try changing the instructions:
  - E.g., `"You are a helpful assistant. Write limericks about Python."`
- Run multiple prompts and observe agent outputs.
- Optional: Create `examples/haiku_agent.py` for experimentation.

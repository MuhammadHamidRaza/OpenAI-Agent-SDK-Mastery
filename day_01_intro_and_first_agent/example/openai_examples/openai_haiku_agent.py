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

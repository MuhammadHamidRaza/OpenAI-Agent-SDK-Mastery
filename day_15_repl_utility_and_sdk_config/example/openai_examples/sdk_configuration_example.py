from agents import Agent, Runner, ModelSettings
import os

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# 1. Global/Default Model Settings (Conceptual)
# You might set default model settings that apply to all agents unless overridden.
# from agents import set_default_model_settings
# set_default_model_settings(ModelSettings(model="gpt-4-turbo", temperature=0.7))

# 2. Agent-Specific Model Settings
# You can pass ModelSettings directly to the Agent constructor.
creative_agent = Agent(
    name="Poet",
    instructions="You are a creative poet.",
    model_settings=ModelSettings(temperature=0.9, model="gpt-3.5-turbo")
)

# 3. Runner-Specific Overrides
# You can override settings for a specific run using the Runner.
# This is useful for one-off tests or dynamic adjustments.
print("Running creative agent with default settings...")
result1 = Runner.run_sync(creative_agent, "Write a short poem about a lonely cloud.")
print(f"Agent 1: {result1.final_output}")

print("\nRunning creative agent with lower temperature for more deterministic output...")
result2 = Runner.run_sync(
    creative_agent,
    "Write a short poem about a lonely cloud.",
    model_settings=ModelSettings(temperature=0.2) # Override for this run
)
print(f"Agent 2: {result2.final_output}")

# 4. Max Turns Configuration
# You can limit the number of turns an agent takes to prevent infinite loops.
loopy_agent = Agent(
    name="Loopy",
    instructions="Always ask a follow-up question."
)

try:
    print("\nRunning loopy agent with max_turns=3...")
    result3 = Runner.run_sync(loopy_agent, "Tell me about yourself.", max_turns=3)
    print(f"Agent 3: {result3.final_output}")
except Exception as e: # Likely MaxTurnsExceeded
    print(f"Agent 3 encountered an error: {e}") 

print("SDK configuration provides fine-grained control over agent behavior.")

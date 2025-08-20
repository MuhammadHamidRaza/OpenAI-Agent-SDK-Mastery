from agents import Agent, Runner, function_tool

@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."
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

from agents import Agent, Runner, function_tool

@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

@function_tool
def multiply(x: int, y: int) -> int:
    return x * y

agent = Agent(name="Calc", instructions="Use tools for math.", tools=[add_numbers, multiply])

# Example usage (not in original, but for completeness)
result = Runner.run_sync(agent, "What is 7 times 5?")
print(result.final_output)

result = Runner.run_sync(agent, "What is 10 plus 20?")
print(result.final_output)

from agents import Agent, Runner

agent = Agent(name="Helper", instructions="Answer concisely.")
Runner.run_sync(agent, "What is 2+2?")
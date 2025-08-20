from agents import Agent, Runner

  

agent = Agent(name="Assistant", instructions="Answer concisely.")

result = Runner.run_sync(agent, "Explain recursion in one short sentence.")

print("Final Output:", result.final_output)

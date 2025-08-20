from agents import WebSearchTool
from agents import Agent, Runner

agent = Agent(
    name="SearchBuddySync",
    instructions="Answer user questions using web search when needed.",
    tools=[WebSearchTool()],
)

# Blocking call for simple scripts
result = Runner.run_sync(agent, "What are the top headlines about climate technology today?")
print(result.final_output)
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel

# ✅ Gemini client setup
client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

# ✅ Define agent with Gemini model
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model
)

# ✅ Run the agent
result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)

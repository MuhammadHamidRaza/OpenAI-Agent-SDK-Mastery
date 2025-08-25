from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

agent = Agent(name="MemoryAssistant", instructions="Reply concisely.", model=model)

# Temporary session (in-memory for this program run)
session = SQLiteSession("conversation_temp")

# Turn 1: store a fact in the session
res1 = Runner.run_sync(agent, "Hi — my name is Sara and I like pizza.", session=session)
print("Turn 1:", res1.final_output)

# Turn 2: follow-up uses session history automatically
res2 = Runner.run_sync(agent, "What's my name?", session=session)
print("Turn 2:", res2.final_output)
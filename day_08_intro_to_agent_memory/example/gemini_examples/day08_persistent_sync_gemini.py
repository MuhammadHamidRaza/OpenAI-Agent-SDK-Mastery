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

agent = Agent(name="PersistentAssistant", instructions="Remember user facts across runs.", model=model)

# Persistent session saved to conversations.db
persistent_session = SQLiteSession("user_123", "conversations.db")

# Save a persistent fact
# Runner.run_sync(persistent_session, "Note: favorite_drink=chai")  # optional helper run to add items
Runner.run_sync(agent, "Remember: my favorite drink is chai.", session=persistent_session)

# Later (after restarting the program), this will still be remembered:
res = Runner.run_sync(agent, "What is my favorite drink?", session=persistent_session)
print(res.final_output)
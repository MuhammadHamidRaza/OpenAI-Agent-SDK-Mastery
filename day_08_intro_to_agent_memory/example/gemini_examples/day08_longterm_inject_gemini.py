from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

agent = Agent(name="LongTermAgent", instructions="Use known user facts where relevant.", model=model)

# Simulated long-term store (could be DB / JSON / vector store)
long_term_store = {
    "user_42": {"favorite_drink": "chai", "city": "Karachi"}
}

# Before running, fetch facts and inject a compact context snippet:
facts = long_term_store.get("user_42", {})
pref_text = f"User facts: favorite_drink={facts.get('favorite_drink','unknown')}, city={facts.get('city','unknown')}\n"

result = Runner.run_sync(agent, f"{pref_text}\nUser: Recommend a coffee shop nearby.")
print(result.final_output)
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

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

agent = Agent(name='Assistant', instructions='Reply briefly.', model=model)

# Manual continuation (no sessions)
res = Runner.run_sync(agent, 'I like Python. Recommend a topic.')
print("Manual 1:", res.final_output)
inputs = res.to_input_list()
inputs.append({'role': 'user', 'content': 'Why that topic?'})
res2 = Runner.run_sync(agent, inputs)
print("Manual 2:", res2.final_output)

# Using sessions (automatic)
session = SQLiteSession('my_chat')
res1 = Runner.run_sync(agent, 'Hi!', session=session)
print("Session 1:", res1.final_output)
res2 = Runner.run_sync(agent, 'What did I ask earlier?', session=session)
print("Session 2:", res2.final_output)
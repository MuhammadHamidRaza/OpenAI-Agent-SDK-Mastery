# session_sync.py
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# ✅ Gemini client setup
client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

agent = Agent(name='Assistant', instructions='Reply briefly.', model=model)
session = SQLiteSession('conversation_123')

res1 = Runner.run_sync(agent, 'What city is the Golden Gate Bridge in?', session=session)
print('1:', res1.final_output)
res2 = Runner.run_sync(agent, 'What state is it in?', session=session)
print('2:', res2.final_output)
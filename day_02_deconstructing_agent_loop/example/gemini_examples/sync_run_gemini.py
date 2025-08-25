# sync_run.py
from agents import Agent, Runner, OpenAIChatCompletionsModel
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

agent = Agent(name='Assistant', instructions='Answer concisely.', model=model)
result = Runner.run_sync(agent, 'Explain recursion in one short sentence.')
print('Final:', result.final_output)
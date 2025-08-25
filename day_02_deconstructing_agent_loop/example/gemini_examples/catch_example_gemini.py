from agents import Agent, Runner, OpenAIChatCompletionsModel
from agents.exceptions import MaxTurnsExceeded, AgentsException
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

agent = Agent(name='Loopy', instructions='Try to answer briefly.', model=model)
try:
    res = Runner.run_sync(agent, 'Do a long task', max_turns=2)
    print(res.final_output)
except MaxTurnsExceeded:
    print('Too many turns — simplify the task or raise max_turns.')
except AgentsException as e:
    print('Agent error:', type(e).__name__, str(e))
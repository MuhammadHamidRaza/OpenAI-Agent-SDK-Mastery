from agents import Agent, Runner, OpenAIChatCompletionsModel
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

agent = Agent(name='Assistant', instructions='Answer concisely.', model=model)
res = Runner.run_sync(agent, 'Explain recursion in 1 sentence')
print('final:', res.final_output)
print('last agent:', res.last_agent)
for item in res.new_items:
    print(type(item).__name__, getattr(item, 'raw_item', None))
# Manually continue if you want:
inputs = res.to_input_list()
inputs.append({'role': 'user', 'content': 'Expand the example.'})
res2 = Runner.run_sync(agent, inputs)
print('Final 2:', res2.final_output)
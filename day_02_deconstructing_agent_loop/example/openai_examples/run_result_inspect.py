from agents import Agent, Runner

agent = Agent(name='Assistant', instructions='Answer concisely.')
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
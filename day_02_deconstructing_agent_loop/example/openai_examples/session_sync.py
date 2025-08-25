# session_sync.py
from agents import Agent, Runner, SQLiteSession

agent = Agent(name='Assistant', instructions='Reply briefly.')
session = SQLiteSession('conversation_123')

res1 = Runner.run_sync(agent, 'What city is the Golden Gate Bridge in?', session=session)
print('1:', res1.final_output)
res2 = Runner.run_sync(agent, 'What state is it in?', session=session)
print('2:', res2.final_output)
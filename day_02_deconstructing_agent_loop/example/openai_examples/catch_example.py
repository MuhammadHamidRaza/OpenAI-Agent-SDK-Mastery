from agents import Agent, Runner
from agents.exceptions import MaxTurnsExceeded, AgentsException

agent = Agent(name='Loopy', instructions='Try to answer briefly.')
try:
    res = Runner.run_sync(agent, 'Do a long task', max_turns=2)
    print(res.final_output)
except MaxTurnsExceeded:
    print('Too many turns — simplify the task or raise max_turns.')
except AgentsException as e:
    print('Agent error:', type(e).__name__, str(e))
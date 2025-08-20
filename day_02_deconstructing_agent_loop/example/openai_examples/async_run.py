import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(name='Assistant', instructions='Answer concisely.')
    result = await Runner.run(agent, 'Write a haiku about recursion in programming.')
    print('Final:', result.final_output)

if __name__ == '__main__':
    asyncio.run(main())

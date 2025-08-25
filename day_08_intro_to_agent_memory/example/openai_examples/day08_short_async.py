import asyncio
from agents import Agent, Runner, SQLiteSession

async def main():
    agent = Agent(name="AsyncMemoryBot", instructions="Be friendly.")
    session = SQLiteSession("async_session_1")
    await Runner.run(agent, "My name is Alex.", session=session)
    result = await Runner.run(agent, "What is my name?", session=session)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
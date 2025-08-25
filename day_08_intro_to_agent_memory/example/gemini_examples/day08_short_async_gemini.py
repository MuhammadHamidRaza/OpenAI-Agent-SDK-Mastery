import asyncio
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=client
)

async def main():
    agent = Agent(name="AsyncMemoryBot", instructions="Be friendly.", model=model)
    session = SQLiteSession("async_session_1")
    await Runner.run(agent, "My name is Alex.", session=session)
    result = await Runner.run(agent, "What is my name?", session=session)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
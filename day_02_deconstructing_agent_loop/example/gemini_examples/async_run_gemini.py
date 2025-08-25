# async_run.py
import asyncio
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

async def main():
    agent = Agent(name='Assistant', instructions='Answer concisely.', model=model)
    result = await Runner.run(agent, 'Write a haiku about recursion in programming.')
    print('Final:', result.final_output)

if __name__ == '__main__':
    asyncio.run(main())
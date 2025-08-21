# day08_correction.py
import asyncio
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

async def main():
    # Gemini client setup
    client = AsyncOpenAI(
        api_key="GEMINI_API_KEY",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Gemini model
    model = OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=client
    )

    agent = Agent(name="Calc", instructions="Answer math questions simply.", model=model)
    session = SQLiteSession("correction_example")

    # initial wrong question/answer
    await Runner.run(agent, "What's 2 + 2?", session=session)
    print("Initial answer saved.")

    # Remove assistant response and user's question (undo)
    await session.pop_item()  # removes assistant's last message
    await session.pop_item()  # removes user's last message

    # Ask corrected question
    res = await Runner.run(agent, "What's 2 + 3?", session=session)
    print("Corrected answer:", res.final_output)

asyncio.run(main())
import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

# ✅ Gemini client setup
client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

async def main():
    agent = Agent(name="Streamer", instructions="Give three quick tips.", model=model)
    result = Runner.run_streamed(agent, input="Give three study tips for today.")

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    print("\n\nFinal Output:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

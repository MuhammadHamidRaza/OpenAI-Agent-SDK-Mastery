import asyncio

from agents import Agent, Runner

from openai.types.responses import ResponseTextDeltaEvent


async def main():
    # make sure `model` is defined (string or model provider object) if you pass it here
    agent = Agent(name="Streamer", instructions="Give three quick tips.")
    result = Runner.run_streamed(agent, input="Give three study tips for today.")

    async for event in result.stream_events():
        # Example: token deltas
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

    # After the stream ends the RunResultStreaming object contains the final output
    print("\n\nFinal Output:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio # Added
from agents import Agent, Runner
import os

# Ensure the OpenAI API key is set
# os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" 

if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

@function_tool
def how_many_jokes() -> int:
    import random

    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="StreamingAssistant",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
    )

    result = Runner.run_streamed(agent, input="Hello")
    print("=== Streaming started ===")

    async for event in result.stream_events():
        # Ignore raw token events
        if event.type == "raw_response_event":
            continue

        # Agent update events
        elif event.type == "agent_updated_stream_event":
            print(f"[Agent Updated] New agent: {event.new_agent.name}")
            continue

        # Item-level events
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(
                    f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}"
                )
            else:
                pass  # Ignore other event types

    


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from agents import Agent, Runner, ItemHelpers, function_tool
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

# Setup Gemini client
client = AsyncOpenAI(
    api_key="YOUR_GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)


# Example tool
@function_tool
def how_many_jokes() -> int:
    import random

    return random.randint(1, 10)


async def main():
    agent = Agent(
        name="StreamingAssistant",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        model=model,
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

import asyncio
from agents import Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Assuming orchestrator is defined in a separate module or within this file
# For simplicity, I'll redefine a minimal orchestrator here for demonstration
# In a real scenario, you'd import it or define it globally.

# Gemini client setup
client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

# --- Specialists ---
# Minimal Researcher and Summarizer for streaming demo
researcher = Agent(
    name="Researcher",
    instructions="Find information.",
    model=model
)

summarizer = Agent(
    name="Summarizer",
    instructions="Summarize information.",
    model=model
)

orchestrator = Agent(
    name="Planner",
    instructions="Coordinate specialists. Hand off to Researcher then Summarizer.",
    handoffs=[researcher, summarizer],
    model=model
)


async def main():
    session = SQLiteSession(user_id="stream_user", db_path="day12_stream.db")
    query = "Summarize the key milestones in AI from 1950 to 2010."

    stream = Runner.run_streamed(orchestrator, query, session=session)
    async for event in stream.stream_events():
        if event.type == "agent_updated_stream_event":
            print(f"[handoff] Active agent → {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            item = event.item
            if getattr(item, "type", "") == "message_output_item" and hasattr(item, "text"):
                print(item.text, end="", flush=True)

    final = await stream.get_final_result()
    print("\n\n--- Final ---\n", final.final_output)

if __name__ == "__main__":
    asyncio.run(main())
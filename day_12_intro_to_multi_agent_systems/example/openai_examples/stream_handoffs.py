import asyncio
from agents import Runner, SQLiteSession
from orchestrated_research_summary import orchestrator # Assuming orchestrator is defined in this module

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
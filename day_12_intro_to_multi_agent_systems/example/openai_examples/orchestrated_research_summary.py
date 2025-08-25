import asyncio
from agents import Agent, Runner, SQLiteSession, trace,function_tool,WebSearchTool

# Optional WebSearchTool (only if available in your env)

# --- Specialists ---
# Researcher: uses web search when present; otherwise returns concise notes.
researcher = Agent(
    name="Researcher",
    handoff_description="Finds current, credible information from the web (or summarizes known info if web search is unavailable).",
    instructions=(
        "Collect relevant facts, stats, and sources about the user's topic. "
        "If WebSearchTool is available, use it. "
        "Return a short bullet list of key findings and any sources."
    ),
    tools=[WebSearchTool()],
)

# Summarizer: writes a concise paragraph from notes
summarizer = Agent(
    name="Summarizer",
    handoff_description="Turns research notes into a concise, well‑structured paragraph.",
    instructions=(
        "Write a single concise paragraph that synthesizes the Researcher's notes. "
        "Be factual, neutral, and readable for a general audience."
    ),
)

# Orchestrator/Planner
orchestrator = Agent(
    name="Planner",
    instructions=(
        "Coordinate specialists. For research tasks, first hand off to Researcher. "
        "Then hand off the notes to Summarizer to produce the final paragraph. "
        "Return the Summarizer's final paragraph to the user."
    ),
    handoffs=[researcher, summarizer],
)

async def main():
    session = SQLiteSession(user_id="day12_user", db_path="day12_multi_agent.db")

    with trace(workflow_name="Research & Summarize", group_id="day12"):
        query = "Research the history of AI and write a one‑paragraph summary."
        result = await Runner.run(orchestrator, query, session=session)
        print("\n--- Final Answer ---\\n", result.final_output)

        # Follow‑up uses the same session (memory)
        followup = "Great. Add one concise source at the end."
        result2 = await Runner.run(orchestrator, followup, session=session)
        print("\n--- Follow‑up ---\\n", result2.final_output)

if __name__ == "__main__":
    asyncio.run(main())

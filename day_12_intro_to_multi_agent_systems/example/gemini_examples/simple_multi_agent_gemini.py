from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client
)

# Math specialist
math_agent = Agent(
    name="MathBuddy",
    handoff_description="Specialist for arithmetic and other math questions.",
    instructions=(
        "You are a math expert. Answer math questions clearly and briefly. "
        "Show only the essential steps if needed."
    ),
    model=model
)

# General helper that can hand off to MathBuddy
general_agent = Agent(
    name="HelperBuddy",
    instructions=(
        "You are a friendly general assistant. "
        "If the user's query involves math or calculations, hand off to MathBuddy. "
        "Otherwise, answer directly and keep it concise."
    ),
    handoffs=[math_agent],
    model=model
)

r1 = Runner.run_sync(general_agent, "What is a bird?")
print("General:", r1.final_output)

r2 = Runner.run_sync(general_agent, "What is 8 plus 5?")
print("Math:", r2.final_output)
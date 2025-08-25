from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Gemini client setup
client = AsyncOpenAI(
    api_key="your-gemini-api-key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", # Or another appropriate Gemini model
    openai_client=client
)

agent = Agent(name="Helper", instructions="Answer concisely.", model=model)
Runner.run_sync(agent, "What is 2+2?")
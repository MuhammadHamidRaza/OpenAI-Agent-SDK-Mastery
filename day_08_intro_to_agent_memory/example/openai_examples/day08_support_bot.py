import asyncio
from agents import Agent, Runner, SQLiteSession

class SupportBot:
    def __init__(self):
        self.agent = Agent(
            name="SupportBot",
            instructions="You are a helpful customer support agent. Be polite and remember conversation history for each user."
        )

    def session_for(self, customer_id: str):
        return SQLiteSession(f"customer_{customer_id}", "support_conversations.db")

    async def chat(self, customer_id: str, message: str):
        session = self.session_for(customer_id)
        result = await Runner.run(self.agent, message, session=session)
        return result.final_output

# Usage
async def main():
    bot = SupportBot()
    print(await bot.chat("123", "Hi, I'm having trouble with order #12345"))
    print(await bot.chat("123", "What was my order number again?"))  # should recall #12345
    print(await bot.chat("456", "Hello, I need help with billing"))  # separate conversation

if __name__ == "__main__":
    asyncio.run(main())
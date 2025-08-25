from agents import Agent, Runner

# Define agents
support_agent = Agent(
    name="SupportAgent",
    instructions="Handle customer FAQs about products."
)

billing_agent = Agent(
    name="BillingAgent",
    instructions="Handle all billing, invoices, and payment-related queries."
)

# Runner with multiple agents
runner = Runner(agents=[support_agent, billing_agent])

async def main():
    # Start with support agent
    result = await runner.run(support_agent, "I have a problem with my last invoice.")
    print(result.final_output)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
# Day 38: Project 4: Real-time Stock Analyst

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 38 of the **OpenAI Agent SDK Mastery** course! You've mastered real-time and voice agents. Today, we combine these advanced concepts in your fourth major project: building a **Real-time Stock Analyst**. This project will demonstrate how to create an agent that can analyze live stock data, integrate with external APIs for real-time information, and provide insightful summaries or predictions based on current market conditions and news. You'll apply your knowledge of custom tool development, real-time processing, and potentially web search to build a dynamic and highly relevant financial intelligence agent.

---

## Project Goal: Real-time Stock Analyst

Your goal is to create an agent that can provide real-time analysis of stock performance. The system should be able to:

1.  **Fetch real-time stock data** for a given ticker symbol.
2.  **Analyze trends** and key metrics.
3.  **Integrate current news/events** that might impact the stock.
4.  **Provide concise insights** or summaries to the user.

### Components We'll Use:

*   **Agent:** The core intelligent entity.
*   **Custom Tool for Stock Data API:** To fetch real-time stock prices, volume, etc.
*   **`WebSearchTool`:** (Optional, but recommended) To fetch recent news related to the stock.
*   **Real-time Processing:** Leveraging asynchronous operations for responsiveness.
*   **`Runner`:** To execute the agent.

---

## Step-by-Step Implementation

### Step 1: Setup and Conceptual Stock Data Tool

We'll create a custom tool that simulates fetching real-time stock data. In a real application, you would integrate with a financial data API (e.g., Alpha Vantage, Finnhub, Twelve Data).

```python
import os
import asyncio
from agents import Agent, Runner
from agents.tools import function_tool, WebSearchTool # WebSearchTool is optional

# Ensure your OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()

# ---
# Conceptual Stock Data API Tool ---
# In a real scenario, you'd use a library like 'requests' to call a real API
# and handle API keys securely via environment variables.

@function_tool
async def get_realtime_stock_data(ticker: str) -> str:
    """Fetches real-time stock data for a given ticker symbol.

    Args:
        ticker: The stock ticker symbol (e.g., "AAPL", "MSFT").

    Returns:
        A string containing real-time stock information.
    """
    print(f"[TOOL]: Fetching real-time data for {ticker.upper()}...")
    await asyncio.sleep(2) # Simulate API call latency

    # Simulated data
    ticker_upper = ticker.upper()
    if ticker_upper == "AAPL":
        return f"Real-time data for AAPL: Price $175.20, Volume 75M, Change +$1.50 (+0.86%)."
    elif ticker_upper == "MSFT":
        return f"Real-time data for MSFT: Price $320.50, Volume 50M, Change -$0.80 (-0.25%)."
    else:
        return f"Real-time data for {ticker_upper}: Not available or invalid ticker."

# Initialize WebSearchTool (optional, requires API key setup for a real search service)
# web_search_tool = WebSearchTool()

print("Conceptual stock data tool ready.")
```

### Step 2: Define the Real-time Stock Analyst Agent

Create your `Agent` instance and provide it with the stock data tool and optionally the web search tool.

```python
# ... (previous code for imports and setup) ...

stock_analyst_agent = Agent(
    name="RealtimeStockAnalyst",
    instructions=(
        "You are a real-time stock market analyst. "
        "Your primary goal is to provide up-to-date stock information and insights. "
        "Use the 'get_realtime_stock_data' tool to fetch current prices and metrics. "
        "Optionally, use web search to find recent news or events impacting the stock. "
        "Summarize the data and news into a concise, actionable insight for the user. "
        "Always be precise with numbers and indicate the source of information. "
    ),
    tools=[get_realtime_stock_data] # Add web_search_tool here if you want to use it
)

print("Real-time Stock Analyst Agent defined.")
```

### Step 3: Implement the Real-time Analysis Loop

We'll create an asynchronous loop to simulate continuous monitoring or on-demand analysis.

```python
# ... (previous code for imports, setup, and agent definition) ...

async def analyze_stock_in_realtime(ticker_symbol: str):
    print(f"\n--- Real-time Analysis for {ticker_symbol.upper()} ---")
    print("Type 'stop' to end analysis.")

    while True:
        user_input = input(f"\n(Enter to refresh, 'stop' to quit for {ticker_symbol.upper()}): ")
        if user_input.lower() == 'stop':
            break

        query = f"Provide a real-time analysis for {ticker_symbol.upper()}, including its current price, volume, and recent news that might affect it."
        
        # Run the agent asynchronously with streaming for real-time feel
        print(f"Agent analyzing {ticker_symbol.upper()}: ", end="", flush=True)
        agent_response_text = ""
        with Runner.run_streamed(stock_analyst_agent, query) as stream:
            async for event in stream:
                if hasattr(event, 'text'):
                    print(event.text, end="", flush=True)
                    agent_response_text += event.text
                elif hasattr(event, 'tool_name'):
                    print(f"\n[Agent using tool: {event.tool_name}]")
                elif hasattr(event, 'output'):
                    print(f"\n[Tool output: {event.output}]")
            final_result = stream.get_final_result()
            agent_response_text = final_result.final_output # Ensure complete output
        print("\n")

        # Optional: Add a small delay before next refresh if not user-triggered
        # await asyncio.sleep(5) 

    print(f"--- Analysis for {ticker_symbol.upper()} Ended ---")

# Run the real-time analysis for a stock
async def main():
    await analyze_stock_in_realtime("AAPL")
    # await analyze_stock_in_realtime("MSFT") # You can run for multiple stocks

if __name__ == "__main__":
    asyncio.run(main())

```

---

## Key Takeaways from Project 4

*   You've built a **real-time agent** that integrates with external data sources (simulated stock API) to provide dynamic insights.
*   You leveraged **asynchronous custom tools** (`get_realtime_stock_data`) to handle external API calls without blocking the main execution flow.
*   **Streaming (`Runner.run_streamed()`)** was crucial for providing a responsive user experience, displaying information as it's fetched and analyzed.
*   This project demonstrates the power of combining agent intelligence with live data for applications requiring up-to-the-minute information.

Congratulations on completing your fourth major project! This project showcases the practical application of real-time agents in a data-intensive domain. Tomorrow, we'll explore **Advanced Multi-Agent Patterns**, delving into more complex collaboration strategies for highly sophisticated AI systems.
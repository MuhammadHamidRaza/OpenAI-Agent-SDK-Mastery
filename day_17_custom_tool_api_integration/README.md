# Day 17: Custom Tool Development & API Integration

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 17 of the **OpenAI Agent SDK Mastery** course! Yesterday, you empowered your agents with the ability to execute code, significantly expanding their computational prowess. Today, we take another leap forward by learning how to build **custom tools that integrate with external APIs**. This skill is paramount for creating truly dynamic and real-world agentic applications. By connecting your agents to third-party services—whether it's a weather API, a CRM, a payment gateway, or a custom internal system—you unlock an almost limitless potential for your agents to perform actions, retrieve data, and automate workflows across the digital landscape. You'll learn the process of designing, implementing, and integrating these API-driven tools effectively.

---

## Why API Integration is Essential for Agents

While built-in tools like web search and code interpreters are powerful, the real world runs on APIs. Almost every modern application, service, and data source exposes an API for programmatic access. By enabling your agents to interact with these APIs, you can:

*   **Access Real-time, Specific Data:** Retrieve live stock prices, flight information, e-commerce product details, or sensor readings.
*   **Perform Actions in External Systems:** Create calendar events, send emails, update database records, process payments, or manage customer support tickets.
*   **Automate Complex Workflows:** Chain together multiple API calls to automate multi-step business processes.
*   **Extend Agent Capabilities Infinitely:** Any service with an API can become a capability of your agent.

API integration transforms your agents from intelligent conversationalists into powerful automation engines that can interact with the entire digital ecosystem.

---

## Designing an API-Driven Custom Tool

When building a custom tool for API integration, consider the following design principles:

1.  **Clear Purpose:** Each tool should have a single, well-defined purpose that maps to one or more API endpoints.
2.  **Input Parameters:** Identify what information the tool needs from the agent (and ultimately the user) to make the API call. These become your function arguments.
3.  **Output Format:** Determine what information the API returns and how you want to present it back to the agent (and potentially the user). Simplify complex API responses into a digestible format.
4.  **Error Handling:** APIs can fail. Implement robust error handling to gracefully manage network issues, invalid inputs, or API-specific errors.
5.  **Authentication:** Securely handle API keys, tokens, or other authentication mechanisms. Avoid hardcoding sensitive credentials.

---

## Example: Building a Weather API Tool

Let's create a tool that fetches current weather information for a given city using a hypothetical weather API. For this example, we'll simulate an API call, but in a real scenario, you would use a library like `requests` to make HTTP requests.

**Prerequisites:**

*   A (hypothetical) API key for a weather service. In a real application, you'd get this from a service like OpenWeatherMap, WeatherAPI, etc.

```python
from agents import Agent, Runner
from agents.tools import function_tool
import os
import requests # You would typically use this for real API calls

# ---
# Configuration ---
# Ensure your OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.")
    print("Please set it before running the agent.")
    exit()

# Hypothetical API Key for the weather service
# In a real scenario, you would get this from an environment variable
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "YOUR_WEATHER_API_KEY_HERE")

@function_tool
def get_current_weather(city: str, unit: str = "celsius") -> str:
    """Fetches the current weather conditions for a specified city.

    Args:
        city: The name of the city (e.g., "London", "New York").
        unit: The unit of temperature, either "celsius" or "fahrenheit". Defaults to "celsius".

    Returns:
        A string describing the current weather, or an error message if data cannot be retrieved.
    """
    if not WEATHER_API_KEY or WEATHER_API_KEY == "YOUR_WEATHER_API_KEY_HERE":
        return "Error: Weather API key not configured."

    # ---
    # Simulate API Call ---
    # In a real application, you would make an HTTP request like this:
    # try:
    #     base_url = "https://api.example.com/weather"
    #     params = {
    #         "q": city,
    #         "appid": WEATHER_API_KEY,
    #         "units": "metric" if unit == "celsius" else "imperial"
    #     }
    #     response = requests.get(base_url, params=params)
    #     response.raise_for_status() # Raise an exception for HTTP errors
    #     data = response.json()
    #     # Process data and return formatted string
    #     temperature = data["main"]["temp"]
    #     description = data["weather"][0]["description"]
    #     return f"The current weather in {city} is {temperature}°{unit.upper()[0]} with {description}."
    # except requests.exceptions.RequestException as e:
    #     return f"Error fetching weather for {city}: {e}"
    # except KeyError:
    #     return f"Could not parse weather data for {city}."

    # For demonstration, we'll return a static response
    if city.lower() == "london":
        return f"The current weather in London is 15°{unit.upper()[0]} and cloudy."
    elif city.lower() == "new york":
        return f"The current weather in New York is 25°{unit.upper()[0]} and sunny."
    else:
        return f"Weather data for {city} is not available."

# Define an agent that can use the weather tool
weather_agent = Agent(
    name="WeatherReporter",
    instructions="You are a helpful assistant that can report current weather conditions. Use the provided tool to get weather information.",
    tools=[get_current_weather]
)

print("Running WeatherReporter agent...")
result = Runner.run_sync(weather_agent, "What's the weather like in London?")
print(f"Agent's response: {result.final_output}")

print("\nRunning WeatherReporter agent for New York in Fahrenheit...")
result2 = Runner.run_sync(weather_agent, "How about New York in Fahrenheit?")
print(f"Agent's response: {result2.final_output}")

print("\nRunning WeatherReporter agent for an unknown city...")
result3 = Runner.run_sync(weather_agent, "What's the weather in Tokyo?")
print(f"Agent's response: {result3.final_output}")

```

**Explanation:**

*   The `get_current_weather` function is decorated with `@function_tool`.
*   It takes `city` and `unit` as arguments, which the LLM will extract from the user\'s prompt.
*   The docstring clearly describes the tool\'s purpose and parameters.
*   The `WEATHER_API_KEY` is retrieved from an environment variable, which is a best practice for sensitive information.
*   The commented-out `requests` code shows how you would make a real API call. The current implementation provides simulated responses for demonstration.

---

## Best Practices for API Integration Tools

*   **Environment Variables for Credentials:** Always store API keys and other sensitive credentials in environment variables, not directly in your code.
*   **Robust Error Handling:** Anticipate and handle various API errors (network issues, rate limits, invalid responses, authentication failures). Provide informative error messages back to the agent.
*   **Rate Limiting and Caching:** For frequently called APIs, implement rate limiting to avoid exceeding API quotas and caching to reduce redundant calls and improve performance.
*   **Clear Tool Descriptions:** Ensure the docstring for your tool is highly descriptive, explaining exactly what the tool does, its parameters, and what it returns. This helps the LLM use it correctly.
*   **Input Validation:** Validate inputs received by your tool function before making API calls to prevent errors and potential security vulnerabilities.
*   **Asynchronous API Calls:** For performance-critical applications, consider making API calls asynchronously if the underlying API client supports it.

---

## Key Takeaways

*   **API integration** is crucial for extending agent capabilities to interact with real-world services and data.
*   Custom tools can be built using `@function_tool` to encapsulate API calls.
*   Design your API tools with clear purpose, defined inputs/outputs, and robust error handling.
*   Always follow best practices for handling sensitive credentials (environment variables) and managing API interactions (rate limiting, caching).

Today, you've gained the power to connect your agents to the vast world of APIs. Tomorrow, we'll put this knowledge into practice by **Implementing Handoffs**, building a multi-agent system where agents collaborate by delegating tasks to each other.
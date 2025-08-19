# Day 24: Input & Output Validation Guardrails

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 24 of the **OpenAI Agent SDK Mastery** course! We've explored how agents can reflect and self-correct, enhancing their internal robustness. Today, we focus on external robustness by diving deeper into **Input and Output Validation Guardrails**. Building upon our introduction to guardrails on Day 14, this session will provide practical techniques for implementing checks that ensure your agent receives appropriate inputs and produces safe, compliant, and correctly formatted outputs. Mastering these validation mechanisms is crucial for preventing unintended behaviors, maintaining data integrity, and building trustworthy AI applications that operate within defined boundaries.

---

## The Critical Role of Validation Guardrails

Even the most intelligent agents can be vulnerable to unexpected or malicious inputs, or they might generate outputs that are inappropriate, incorrect, or outside the desired format. Validation guardrails act as essential checkpoints to prevent these issues:

### Input Validation Guardrails:

*   **Purpose:** To filter, sanitize, or reject user inputs before they reach the agent's core logic or the LLM.
*   **Why needed:**
    *   **Preventing Malicious Inputs:** Blocking prompt injection attempts (covered in more detail tomorrow), SQL injection, or other attack vectors.
    *   **Ensuring Relevance:** Filtering out queries that are off-topic or outside the agent's defined scope.
    *   **Data Type/Format Enforcement:** Ensuring inputs conform to expected types (e.g., a number for a calculation, a valid date format).
    *   **Content Moderation:** Detecting and blocking harmful, offensive, or inappropriate language.

### Output Validation Guardrails:

*   **Purpose:** To inspect, modify, or reject the agent's generated responses or tool outputs before they are delivered to the user or external systems.
*   **Why needed:**
    *   **Safety and Compliance:** Preventing the generation of harmful, biased, or non-compliant content.
    *   **Format Enforcement:** Ensuring outputs adhere to a specific structure (e.g., JSON, a specific report format).
    *   **Accuracy Checks:** (Conceptual) In some cases, cross-referencing outputs with known facts or external systems for basic accuracy.
    *   **PII Redaction:** Removing Personally Identifiable Information from responses.
    *   **Length Control:** Ensuring responses are not excessively long or short.

---

## Implementing Validation Guardrails in Practice

The OpenAI Agents SDK provides mechanisms to integrate guardrails, often through specific classes or by allowing you to inject custom validation logic into the agent's pipeline. While the exact implementation might vary, the general approach involves defining a validation function or class and then attaching it to the agent or runner.

### Example: Input Validation - Profanity Filter

Let's create a simple input guardrail that checks for profanity. If profanity is detected, the agent will refuse to process the request.

```python
from agents import Agent, Runner
import os
import re

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define a simple list of profane words for demonstration
PROFANITY_LIST = ["badword1", "badword2", "swearword"]

def contains_profanity(text: str) -> bool:
    """Checks if the given text contains any words from the profanity list.
    This is a very basic example; real-world solutions would use more robust libraries.
    """
    text_lower = text.lower()
    for word in PROFANITY_LIST:
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower): # Use regex for whole word match
            return True
    return False

# Define a custom input validation function
def profanity_input_validator(input_message: str) -> bool:
    if contains_profanity(input_message):
        print("\n[GUARDRAIL BLOCKED]: Input contains profanity. Request rejected.")
        return False # Return False to block the input
    return True # Return True to allow the input

# Define the agent
polite_agent = Agent(
    name="PoliteAssistant",
    instructions="You are a polite and helpful assistant. You do not respond to inappropriate language."
)

print("--- Testing Input Validation Guardrail ---")

# Scenario 1: Clean input
query1 = "Hello, how are you today?"
print(f"\nUser: {query1}")
# Assuming the SDK allows passing custom validators to run_sync or agent config
# For demonstration, we'll manually check before running
if profanity_input_validator(query1):
    result1 = Runner.run_sync(polite_agent, query1)
    print(f"Agent: {result1.final_output}")

# Scenario 2: Profane input
query2 = "This is a badword1 query."
print(f"\nUser: {query2}")
if profanity_input_validator(query2):
    result2 = Runner.run_sync(polite_agent, query2)
    print(f"Agent: {result2.final_output}")
else:
    print("Agent did not process the profane query.")

```

*Note: The OpenAI Agents SDK might have specific `InputGuardrail` or `OutputGuardrail` classes or a `guardrails` parameter in `Runner.run()` that you would use to integrate these validators. The example above demonstrates the core logic of a validator function.* The `default_api` does not expose direct guardrail integration, so this remains conceptual for the SDK.

### Example: Output Validation - PII Redaction (Conceptual)

Let's imagine an output guardrail that redacts Personally Identifiable Information (PII) like email addresses from the agent's response.

```python
# ... (imports and setup) ...

def redact_pii_output_validator(output_message: str) -> str:
    """Redacts email addresses from the output message."
    # This is a simple regex for demonstration; real PII detection is more complex.
    redacted_output = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED_EMAIL]', output_message)
    if redacted_output != output_message:
        print("\n[GUARDRAIL APPLIED]: PII (email) redacted from output.")
    return redacted_output

# Define the agent
info_agent = Agent(
    name="InfoAssistant",
    instructions="You provide information, but must protect sensitive data."
)

print("--- Testing Output Validation Guardrail ---")

# Scenario: Agent generates an email address
# Assuming the SDK allows post-processing of output or direct output guardrail integration
raw_agent_output = "Please contact me at user@example.com for more details."
print(f"\nAgent's raw output: {raw_agent_output}")

processed_output = redact_pii_output_validator(raw_agent_output)
print(f"Agent's processed output: {processed_output}")

raw_agent_output_2 = "My name is John Doe."
print(f"\nAgent's raw output: {raw_agent_output_2}")
processed_output_2 = redact_pii_output_validator(raw_agent_output_2)
print(f"Agent's processed output: {processed_output_2}")

```

---

## Key Considerations for Validation Guardrails

*   **Specificity:** Guardrails should be as specific as possible to avoid false positives or negatives.
*   **Performance:** Complex validation logic can introduce latency. Optimize your guardrails for efficiency.
*   **Layered Approach:** Combine multiple guardrails (e.g., content moderation, PII detection, format validation) for comprehensive protection.
*   **Transparency:** Inform users when a guardrail has been triggered (e.g., "Your input was blocked due to inappropriate content.").
*   **Continuous Improvement:** Regularly review and update your guardrails based on new threats or evolving requirements.
*   **LLM vs. Hardcoded:** While LLMs can perform some moderation, hardcoded rules are often more reliable for critical safety and compliance checks.

---

## Key Takeaways

*   **Input Validation Guardrails** protect your agent from inappropriate, malicious, or malformed inputs.
*   **Output Validation Guardrails** ensure that the agent's responses are safe, compliant, and correctly formatted.
*   Implementing these guardrails is crucial for building **robust, secure, and trustworthy** AI applications.
*   They act as essential checkpoints in the agent's pipeline, preventing unintended behaviors and maintaining control.

Today, you've learned practical ways to secure your agents through validation. Tomorrow, we'll focus on a specific and critical security concern: **Mitigating Prompt Injection Attacks**, understanding how to protect your agents from malicious attempts to hijack their behavior.
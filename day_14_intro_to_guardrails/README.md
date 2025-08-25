# Day 14: Intro to `Guardrails`

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

## Course Overview

Welcome to **Day 14** of the *OpenAI Agent SDK Mastery* course. As agents gain power and autonomy (tools, memory, multi-agent handoffs), we must add safety, reliability, and policy enforcement around them. **Guardrails** are the programmable safety layer that checks inputs, outputs, and agent behavior so you can deploy agents responsibly.

This VIP lesson collects conceptual background, practical patterns, real-world use cases, benefits, and production-ready code examples (including the robust site-provided input/output guardrail patterns). Read through, try the examples, and adapt the guardrails to your product policies.

---

# 1. Why Guardrails Matter

LLM-based agents are powerful but fallible. Without constraints they can:

- Produce unsafe, biased, or toxic outputs.
- Misinterpret prompts or follow malicious instructions (prompt injection).
- Make harmful tool calls (e.g., destructive actions, sensitive-data leaks).
- Consume expensive compute on malicious or irrelevant queries.

**Guardrails** mitigate these risks by validating and (optionally) blocking or sanitizing *before* the expensive model runs (input guardrails) and *after* the agent produces an answer (output guardrails). They are essential for safety, compliance, cost-control, and user trust.

---

# 2. Types of Guardrails

**Input Guardrails** — run on the user input before the agent's main model executes.

*Purpose:* Stop bad or out-of-scope requests early (saves cost, prevents abuse).

**Output Guardrails** — run on the final agent output before it reaches the user.

*Purpose:* Ensure the final response is safe, policy-compliant, and correctly formatted.

**Behavioral / Execution Guardrails** — monitor the agent loop to prevent runaway behavior: excessive tool calls, infinite loops, or unauthorized actions.

*Examples:* limits on tool invocation, token budget guards, or max-turns enforcement.

---

# 3. Tripwires — immediate stops on violations

Guardrails can return a result that signals a **tripwire**. When a tripwire is triggered the Runner raises a specific exception (e.g., `InputGuardrailTripwireTriggered` or `OutputGuardrailTripwireTriggered`) and halts execution. This immediate stop is useful to:

- Prevent expensive model runs.
- Return a controlled error message to the user.
- Log and audit malicious/unsafe attempts.

---

# 4. Design Patterns & Best Practices

- **Run cheap models in guardrails.** Use a small/fast model for guardrail checks so you block abuse cheaply.
- **Policy-first approach.** Define guardrail rules as codified policy objects (keywords, regex, schema validators, intent classifiers) so they are auditable and maintainable.
- **Fail-closed for safety-critical flows.** When in doubt (e.g., potential PHI leak), block or escalate instead of allowing a risky response.
- **Log and alert.** When a tripwire triggers, log the event, collect trace/span metadata, and notify operators for investigation.
- **Have user-friendly fallbacks.** When blocking, return a helpful message explaining why and offer alternatives when appropriate.
- **Attach guardrails to an Agent.** Guardrails are typically agent-specific (different agents have different policies), so keep them colocated with the Agent definition for clarity.
- **Use both input & output guardrails.** Input guardrails stop malicious prompts early; output guardrails catch things that slipped through the agent.

---

# 5. Real-World Use Cases

- **Customer Support:** Block attempts to exfiltrate account data, prevent unauthorized actions (refunds, deletions) unless additional authorization is present.
- **Healthcare:** Prevent sharing of PHI, block unsafe medical recommendations, and ensure clinician-only operations are restricted.
- **Finance:** Prevent leaking or requesting credit-card data and block instructions that could enable fraud.
- **Kid-Facing Chatbots:** Enforce family-friendly language, disallow adult topics, and ensure content is age-appropriate.
- **Internal Developer Tools:** Block commands that could delete production data unless executed with proper authorization.
- **Cost Control:** Detect and block users trying to abuse a high-cost model with repeated or irrelevant prompts.

---

# 6. Benefits of Guardrails

- **Safety:** Reduce harmful outputs and stop unsafe actions before they happen.
- **Compliance:** Enforce legal and regulatory constraints (GDPR, HIPAA, PCI-DSS) through automated checks.
- **Reliability:** Ensure outputs follow required schemas and formats.
- **Cost-efficiency:** Prevent wasteful runs of expensive models on malicious or irrelevant inputs.
- **Trust:** Users and stakeholders gain confidence in predictable, auditable agent behavior.

---

# 7. Implementation: Conceptual Flow

**Input guardrail flow**

1. Runner receives user input for an Agent.
2. Runner executes the agent's input guardrails (in order). Each guardrail returns a `GuardrailFunctionOutput`.
3. If any guardrail `tripwire_triggered == True`, Runner raises `InputGuardrailTripwireTriggered` and stops.
4. Otherwise the main agent run proceeds.

**Output guardrail flow**

1. Agent produces a final output.
2. Runner executes the agent's output guardrails on that output.
3. If a guardrail `tripwire_triggered == True`, Runner raises `OutputGuardrailTripwireTriggered`.
4. Otherwise the result is returned to the user.

---

# 8. Production-ready Examples (site-provided patterns)

Below are the authoritative examples of input and output guardrails as implemented with the Agents SDK. These examples run a small guardrail agent under the hood and return a `GuardrailFunctionOutput` that indicates whether a tripwire fired.

> **Note:** These examples come from the SDK documentation patterns. They demonstrate how to use the `input_guardrail`/`output_guardrail` decorators, the `GuardrailFunctionOutput` type, and the specific tripwire exceptions.

## 8.1 Input guardrail example — detect "math homework"

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)

class MathHomeworkOutput(BaseModel):
    is_math_homework: bool
    reasoning: str

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking you to do their math homework.",
    output_type=MathHomeworkOutput,
)


@input_guardrail
async def math_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math_homework,
    )


agent = Agent(  
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    input_guardrails=[math_guardrail],
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")

    except InputGuardrailTripwireTriggered:
        print("Math homework guardrail tripped")
```

### Explanation

- `guardrail_agent` is a lightweight agent whose `output_type` is a Pydantic model describing the guardrail decision.
- `math_guardrail` runs the `guardrail_agent` on the incoming input and inspects `result.final_output.is_math_homework`.
- If the guardrail sets `tripwire_triggered=True`, the Runner raises `InputGuardrailTripwireTriggered` and halts the main run.

---

## 8.2 Output guardrail example — detect math in the agent's reply

```python
from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    output_guardrail,
)

class MessageOutput(BaseModel):
    response: str

class MathOutput(BaseModel):
    reasoning: str
    is_math: bool

guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the output includes any math.",
    output_type=MathOutput,
)

@output_guardrail
async def math_guardrail(  
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_math,
    )

agent = Agent(
    name="Customer support agent",
    instructions="You are a customer support agent. You help customers with their questions.",
    output_guardrails=[math_guardrail],
    output_type=MessageOutput,
)

async def main():
    # This should trip the guardrail
    try:
        await Runner.run(agent, "Hello, can you help me solve for x: 2x + 3 = 11?")
        print("Guardrail didn't trip - this is unexpected")

    except OutputGuardrailTripwireTriggered:
        print("Math output guardrail tripped")
```

### Explanation

- The output guardrail runs after the agent generates a candidate response.
- We run a small `guardrail_agent` on the candidate text and check an `is_math` boolean.
- If `is_math` is true the guardrail triggers and `OutputGuardrailTripwireTriggered` is raised.

---

# 9. How to Use These Patterns in Production

1. **Start small.** Implement a simple keyword/intent check guardrail and iterate.
2. **Use a small/fast model for the guardrail agent.** It should be cheap and deterministic where possible.
3. **Log all tripwires with trace/span IDs.** This helps diagnose false positives and potential abuse.
4. **Provide a remediation strategy.** If a tripwire blocks a user, give a clear, helpful message and a path to appeal or rephrase.
5. **Combine checks.** Use input + output guardrails for defense-in-depth.
6. **Version guardrails.** Because policies change, version your guardrail rules and record which version ran for each request.


# Day 10: Tracing for Observability

## Key Concepts:

*   **Tracing:** Capturing a detailed, step-by-step timeline of an agent's run.
*   **Spans:** Individual operations within a trace (e.g., agent run, tool call, LLM generation).
*   **Viewing Traces:** Traces are sent to the OpenAI platform and can be viewed in the OpenAI Traces Dashboard.
*   **Disabling Tracing:** Can be disabled for a single run or globally using an environment variable.
*   **Custom Traces and Spans:** Grouping multiple agent runs or tracking specific operations.

## Examples:

Refer to the `README.md` for code examples demonstrating:
*   Basic tracing with a tool.
*   Disabling tracing.
*   Custom traces with `trace()`.
*   Custom spans with `span()`.

## Notes / Tips:

*   Tracing is crucial for debugging, understanding, and optimizing agent behavior.
*   Use clear names for custom traces and spans to improve readability.
*   Be aware of the default tracing behavior and how to disable it if needed.
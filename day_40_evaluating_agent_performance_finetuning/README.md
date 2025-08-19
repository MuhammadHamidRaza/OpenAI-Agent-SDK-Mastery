# Day 40: Evaluating Agent Performance & Fine-Tuning

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 40 of the **OpenAI Agent SDK Mastery** course! You've built sophisticated agents and multi-agent systems. Now, as you prepare to deploy these intelligent applications, a critical question arises: How do you know if your agent is performing well? Today, we delve into **Evaluating Agent Performance and Fine-Tuning**. This session will equip you with the knowledge to define meaningful metrics, collect relevant data, and systematically assess your agent's effectiveness. We'll also explore the concept of fine-tuning—both the underlying LLMs and your agent's configurations—to continuously improve its accuracy, efficiency, and overall utility. By the end of today, you'll have a framework for building and maintaining high-performing AI agents.

---

## The Importance of Evaluation

Without proper evaluation, it's impossible to know if your agent is meeting its objectives, if recent changes have improved or degraded performance, or if it's ready for production. Evaluation is crucial for:

*   **Measuring Success:** Quantifying how well the agent achieves its intended goals.
*   **Identifying Weaknesses:** Pinpointing areas where the agent struggles (e.g., specific query types, tool failures, reasoning errors).
*   **Driving Improvement:** Providing data-driven insights to guide iterative development and optimization.
*   **Ensuring Quality:** Maintaining a high standard of performance and reliability over time.
*   **Justifying Investment:** Demonstrating the value and ROI of your AI agent solution.

---

## Key Performance Metrics for Agents

Agent performance can be assessed using a combination of quantitative and qualitative metrics:

### 1. Task Success Rate

*   **Definition:** The percentage of times the agent successfully completes its primary task (e.g., answers a question correctly, performs a requested action, generates a valid report).
*   **Measurement:** Requires defining what constitutes "success" and often involves human review or automated checks against ground truth.

### 2. Accuracy and Relevance

*   **Definition:** How factually correct and contextually appropriate the agent's responses are.
*   **Measurement:** Human evaluation (e.g., Likert scale ratings), comparison against a golden dataset, or automated checks for factual consistency (e.g., with RAG, checking if answers are grounded in retrieved documents).

### 3. Latency (Response Time)

*   **Definition:** The time taken for the agent to process a query and provide a response.
*   **Measurement:** Milliseconds or seconds, typically measured from input receipt to final output delivery. Important for real-time applications.

### 4. Cost

*   **Definition:** The monetary cost associated with each agent interaction (primarily LLM API calls and tool usage).
*   **Measurement:** Track token usage, API calls, and compute resources.

### 5. User Satisfaction (Qualitative)

*   **Definition:** How satisfied users are with the agent's performance, helpfulness, and overall experience.
*   **Measurement:** User surveys, feedback forms, NPS (Net Promoter Score), or implicit signals like repeat usage.

### 6. Robustness and Safety

*   **Definition:** How well the agent handles edge cases, adversarial inputs (prompt injection), and avoids generating harmful content.
*   **Measurement:** Adversarial testing, guardrail tripwire counts, human review for safety violations.

---

## Data Collection for Evaluation

To evaluate effectively, you need data. This can come from:

*   **Production Logs:** Record all agent inputs, outputs, intermediate steps (traces), tool calls, and any errors.
*   **Human Feedback:** Implement mechanisms for users to provide feedback (e.g., thumbs up/down, free-text comments).
*   **Golden Datasets:** Curated sets of input-output pairs with known correct answers, used for automated testing and regression analysis.
*   **A/B Testing:** Deploying different agent versions to a subset of users to compare performance metrics.

---

## Fine-Tuning for Improvement

Once you've identified areas for improvement through evaluation, **fine-tuning** is the process of adjusting your agent to enhance its performance. This can involve:

### 1. Prompt Engineering and Instruction Refinement

*   **Concept:** Iteratively improving the agent's system instructions to guide the LLM more effectively.
*   **How it works:** Based on evaluation results, modify the agent's `instructions` to address specific failure modes (e.g., clarify ambiguity, emphasize certain behaviors, add examples).
*   **Benefits:** Often the quickest and most cost-effective way to improve performance.

### 2. Tool Refinement

*   **Concept:** Improving the reliability, accuracy, or efficiency of your custom tools.
*   **How it works:** Debug tool code, enhance error handling, optimize API calls, or refine tool descriptions to help the LLM use them correctly.

### 3. Data Augmentation for RAG

*   **Concept:** Improving the quality and coverage of your long-term memory (vector store) for RAG-based agents.
*   **How it works:** Add more relevant documents, improve chunking strategies, or update embeddings.

### 4. Model Parameter Tuning

*   **Concept:** Adjusting LLM generation parameters (e.g., `temperature`, `top_p`, `max_tokens`) to achieve desired output characteristics.
*   **How it works:** Experiment with different `ModelSettings` (as discussed on Day 35) and evaluate the impact on performance metrics.

### 5. LLM Fine-Tuning (Advanced)

*   **Concept:** Training a pre-trained LLM on a smaller, task-specific dataset to adapt its behavior to your specific domain or use case.
*   **How it works:** Requires a dataset of input-output pairs that demonstrate the desired behavior. This is typically done via LLM provider APIs.
*   **Benefits:** Can lead to significant improvements in accuracy and adherence to specific styles/formats.
*   **Considerations:** More complex, time-consuming, and costly than prompt engineering. Requires high-quality training data.

---

## Example: Conceptual Evaluation Loop

```python
from agents import Agent, Runner
import os

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# Define a simple agent for demonstration
qa_agent = Agent(
    name="EvaluatedQAAgent",
    instructions="You are a helpful assistant that answers factual questions concisely."
)

# ---
Simulated Evaluation Data ---
# In a real scenario, this would come from logs, human feedback, or a test dataset.
EVAL_DATA = [
    {"query": "What is the capital of France?", "expected_answer": "Paris", "type": "factual"},
    {"query": "Who painted the Mona Lisa?", "expected_answer": "Leonardo da Vinci", "type": "factual"},
    {"query": "Tell me a joke.", "expected_answer": "(a joke)", "type": "creative"},
    {"query": "What is 10 + 5?", "expected_answer": "15", "type": "math"},
]

def evaluate_agent(agent: Agent, test_data: list) -> dict:
    """Simulates evaluating an agent against a test dataset."""
    results = {"total_queries": len(test_data), "correct_answers": 0, "latency_sum": 0, "cost_sum": 0}

    print("\n--- Starting Agent Evaluation ---")
    for i, item in enumerate(test_data):
        query = item["query"]
        expected = item["expected_answer"]
        print(f"\nQuery {i+1}: {query}")

        start_time = time.time()
        result = Runner.run_sync(agent, query)
        end_time = time.time()

        actual_answer = result.final_output
        latency = end_time - start_time
        # cost = result.token_usage * price_per_token # Conceptual cost calculation

        print(f"  Expected: {expected}")
        print(f"  Actual: {actual_answer}")
        print(f"  Latency: {latency:.2f}s")

        # Simple correctness check (for factual questions)
        if item["type"] == "factual" and expected.lower() in actual_answer.lower():
            results["correct_answers"] += 1
            print("  Status: Correct")
        elif item["type"] == "creative" or item["type"] == "math":
            # For creative/math, a more sophisticated check would be needed
            print("  Status: Reviewed (manual check needed for creative/math)")
        else:
            print("  Status: Incorrect")

        results["latency_sum"] += latency
        # results["cost_sum"] += cost

    print("\n--- Evaluation Summary ---")
    accuracy = (results["correct_answers"] / results["total_queries"]) * 100
    avg_latency = results["latency_sum"] / results["total_queries"]
    print(f"Accuracy (Factual): {accuracy:.2f}%")
    print(f"Average Latency: {avg_latency:.2f}s")
    # print(f"Total Estimated Cost: ${results["cost_sum"]:.4f}")
    return results

import time # Import time for latency calculation

evaluate_agent(qa_agent, EVAL_DATA)

print("\n--- Fine-Tuning Example (Conceptual) ---")
print("Based on evaluation, if factual accuracy is low, we might refine instructions:")

# Refined agent instructions
refined_qa_agent = Agent(
    name="RefinedQAAgent",
    instructions=(
        "You are a highly accurate and concise factual assistant. "
        "Prioritize factual correctness above all else. "
        "If you are unsure of an answer, state that you don't know rather than guessing."
    )
)

print("\nRe-evaluating with refined agent...")
evaluate_agent(refined_qa_agent, EVAL_DATA)

```

**Explanation:**

*   The `evaluate_agent` function simulates running the agent against a predefined `EVAL_DATA` set.
*   It calculates basic metrics like correctness (for factual questions) and latency.
*   The example then conceptually shows how, based on evaluation results, you might refine the agent's instructions and re-evaluate to see the impact.

---

## Key Takeaways

*   **Evaluation** is a continuous process essential for measuring, understanding, and improving agent performance.
*   Key metrics include **task success rate, accuracy, relevance, latency, cost, user satisfaction, robustness, and safety.**
*   Data for evaluation comes from production logs, human feedback, and golden datasets.
*   **Fine-tuning** involves iteratively improving the agent through prompt engineering, tool refinement, data augmentation (for RAG), model parameter tuning, and (for advanced cases) LLM fine-tuning.
*   A systematic evaluation-fine-tuning loop is crucial for building and maintaining high-performing AI agents.

Today, you've learned how to measure and improve your agent's effectiveness. Tomorrow, we'll delve into **Production Best Practices**, covering essential considerations for deploying your AI agents at scale in real-world environments.
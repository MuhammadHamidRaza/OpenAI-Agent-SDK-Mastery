# Day 29: Vector Stores and RAG

[![Proprietary License](https://img.shields.io/badge/license-proprietary-red.svg)](../LICENSE)

---

### **Course Overview**

Welcome to Day 29 of the **OpenAI Agent SDK Mastery** course! Yesterday, we introduced the concept of long-term memory and the role of vector stores in enabling agents to access vast external knowledge. Today, we dive into the practical implementation of **Retrieval-Augmented Generation (RAG)**. You'll learn how to connect your agent to a vector store, embed your own documents, perform semantic searches, and use the retrieved information to augment your agent's responses. This hands-on session will empower your agents with the ability to provide accurate, up-to-date, and contextually relevant answers by leveraging external data sources, significantly reducing hallucinations and enhancing factual grounding.

---

## Recap: What is RAG and Why is it Important?

**Retrieval-Augmented Generation (RAG)** is a technique that enhances the capabilities of Large Language Models (LLMs) by allowing them to retrieve relevant information from an external knowledge base before generating a response. Instead of relying solely on the knowledge encoded during their training, RAG-enabled LLMs can access and incorporate real-time, proprietary, or highly specific data.

**Why RAG is Crucial:**

*   **Reduces Hallucinations:** Grounds the LLM's responses in factual, verifiable information.
*   **Accesses Up-to-Date Information:** Overcomes the LLM's knowledge cut-off date.
*   **Leverages Proprietary Data:** Allows agents to answer questions based on your organization's internal documents, policies, or databases.
*   **Improves Accuracy and Relevance:** Provides more precise and contextually appropriate answers.
*   **Reduces Fine-Tuning Needs:** Often, RAG can achieve similar results to fine-tuning for specific knowledge domains, but with less effort and cost.

---

## The RAG Pipeline with Vector Stores

The RAG process typically involves two main phases:

### Phase 1: Indexing (Offline Process)

This phase involves preparing your external knowledge base for retrieval. It's usually done once or periodically when your data changes.

1.  **Data Loading:** Load your documents (e.g., PDFs, text files, web pages, database records).
2.  **Text Splitting/Chunking:** Break down large documents into smaller, manageable chunks. This is important because embeddings work best on smaller, coherent pieces of text, and LLMs have context window limits.
3.  **Embedding Generation:** Convert each text chunk into a numerical vector (embedding) using an embedding model (e.g., OpenAI's `text-embedding-ada-002`).
4.  **Vector Storage:** Store these embeddings (along with their original text content or a reference to it) in a **Vector Store**.

### Phase 2: Retrieval and Generation (Online Process)

This phase happens in real-time when the agent receives a query.

1.  **Query Embedding:** The user's query is also converted into an embedding using the *same* embedding model used during indexing.
2.  **Semantic Search:** The query embedding is used to perform a similarity search in the vector store, finding the top-K (e.g., top 3 or 5) most semantically similar document chunks.
3.  **Context Augmentation:** The retrieved document chunks are then added to the prompt that is sent to the LLM, along with the original user query.
4.  **Augmented Generation:** The LLM generates a response, now having access to the relevant external information, leading to a more informed and accurate answer.

---

## Practical Implementation: Connecting to a Vector Store

While setting up a full vector store (like Pinecone, Chroma, or FAISS) and ingesting data is a separate process, we can conceptually demonstrate how an agent would interact with it. For this example, we'll simulate the vector store and retrieval process.

**Prerequisites:**

*   An embedding model (e.g., from OpenAI, Hugging Face).
*   A vector store client library (e.g., `pinecone-client`, `chromadb`).

```python
from agents import Agent, Runner
from agents.tools import function_tool
import os
# from openai import OpenAI # For actual embedding generation

# Ensure API key is set
if "OPENAI_API_KEY" not in os.environ:
    print("Please set the OPENAI_API_KEY environment variable.")
    exit()

# ---
# Conceptual Vector Store and Embedding Function ---
# In a real application, you would use a library like OpenAI's API to get embeddings
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
# def get_embedding(text, model="text-embedding-ada-002"):
#     text = text.replace("\n", " ")
#     return client.embeddings.create(input=[text], model=model).data[0].embedding

# Simulate a simple in-memory vector store for demonstration
# In reality, this would be a persistent database like Pinecone, Chroma, etc.
DOCUMENTS = [
    {"id": "doc1", "content": "The capital of France is Paris. It is known for the Eiffel Tower.", "embedding": [0.1, 0.2, 0.3]}, # Placeholder embedding
    {"id": "doc2", "content": "The Amazon rainforest is the largest rainforest in the world.", "embedding": [0.4, 0.5, 0.6]}, # Placeholder embedding
    {"id": "doc3", "content": "Photosynthesis is the process by which plants convert light energy into chemical energy.", "embedding": [0.7, 0.8, 0.9]},
    {"id": "doc4", "content": "The human heart has four chambers: two atria and two ventricles.", "embedding": [0.15, 0.25, 0.35]}
]

def simulate_semantic_search(query_embedding: list, top_k: int = 2) -> list:
    """Simulates finding top_k most similar documents based on embedding similarity."
    # In a real vector store, this would be an efficient similarity search.
    # For simplicity, we'll just return some relevant documents based on keywords.
    query_text = "".join(str(x) for x in query_embedding) # Dummy conversion
    results = []
    if "paris" in query_text.lower() or "france" in query_text.lower():
        results.append(DOCUMENTS[0])
    if "rainforest" in query_text.lower() or "amazon" in query_text.lower():
        results.append(DOCUMENTS[1])
    if "plant" in query_text.lower() or "energy" in query_text.lower():
        results.append(DOCUMENTS[2])
    if "heart" in query_text.lower() or "chamber" in query_text.lower():
        results.append(DOCUMENTS[3])
    return results[:top_k]

@function_tool
def retrieve_document_chunks(query: str) -> str:
    """Retrieves relevant document chunks from the knowledge base based on a query.

    Args:
        query: The user's query or question.

    Returns:
        A string containing the concatenated content of retrieved documents.
    """
    # In a real RAG setup:
    # 1. Get embedding for the query
    # query_embedding = get_embedding(query)
    # 2. Perform semantic search in vector store
    # retrieved_chunks = vector_store_client.query(query_embedding, top_k=3)

    # Simulate retrieval
    simulated_query_embedding = [0.1, 0.2, 0.3] # Placeholder
    retrieved_docs = simulate_semantic_search(simulated_query_embedding, top_k=2)
    
    if not retrieved_docs:
        return "No relevant information found in the knowledge base."
    
    # Concatenate content of retrieved documents
    context_text = "\n\n".join([doc["content"] for doc in retrieved_docs])
    return context_text

# Define an agent that uses the retrieval tool
rag_agent = Agent(
    name="RAGAssistant",
    instructions=(
        "You are a knowledgeable assistant. "
        "Use the 'retrieve_document_chunks' tool to find relevant information from the knowledge base "
        "before answering questions. "
        "Always base your answers on the retrieved information if available. "
        "If the retrieved information is insufficient, state that you cannot answer fully." 
    ),
    tools=[retrieve_document_chunks]
)

print("---"" Testing RAG Agent ---")

query1 = "What is the capital of France and what is it known for?"
print(f"\nUser: {query1}")
result1 = Runner.run_sync(rag_agent, query1)
print(f"Agent: {result1.final_output}")

query2 = "Tell me about photosynthesis."
print(f"\nUser: {query2}")
result2 = Runner.run_sync(rag_agent, query2)
print(f"Agent: {result2.final_output}")

query3 = "What are the main parts of the human heart?"
print(f"\nUser: {query3}")
result3 = Runner.run_sync(rag_agent, query3)
print(f"Agent: {result3.final_output}")

query4 = "Tell me about something completely unrelated to the documents."
print(f"\nUser: {query4}")
result4 = Runner.run_sync(rag_agent, query4)
print(f"Agent: {result4.final_output}")

```

**Explanation:**

*   The `retrieve_document_chunks` function acts as our RAG tool. In a real scenario, it would call an embedding model and then query a vector store.
*   The `rag_agent` is instructed to *always* use this tool to find information before answering.
*   When the agent receives a query, it calls `retrieve_document_chunks`. The output of this tool (the relevant document chunks) is then provided back to the LLM as context.
*   The LLM then generates its answer based on this augmented context.

---

## Key Considerations for RAG Implementation

*   **Chunking Strategy:** How you split your documents into chunks significantly impacts retrieval quality. Experiment with different sizes and overlaps.
*   **Embedding Model Choice:** The quality of your embeddings directly affects semantic search accuracy. Choose a model appropriate for your data and task.
*   **Vector Store Selection:** Consider factors like scalability, cost, features (filtering, hybrid search), and ease of use.
*   **Prompt Engineering for RAG:** Craft your LLM prompt to clearly instruct it to use the retrieved context and to handle cases where no relevant information is found.
*   **Evaluation:** Measure the effectiveness of your RAG system (e.g., retrieval accuracy, answer relevance, reduction in hallucinations).

---

## Key Takeaways

*   **Retrieval-Augmented Generation (RAG)** is a powerful technique to enhance LLM accuracy and relevance by integrating external knowledge.
*   **Vector Stores** are essential for storing and efficiently retrieving document embeddings through semantic search.
*   The RAG pipeline involves **indexing** (loading, chunking, embedding, storing) and **retrieval & generation** (query embedding, semantic search, context augmentation, LLM response).
*   By implementing RAG, your agents can provide factual, up-to-date, and contextually rich answers, leveraging your own data.

Today, you've gained practical insights into building knowledge-aware agents. Tomorrow, we'll explore **Advanced Memory Optimization** techniques to further enhance the efficiency and effectiveness of your agent's memory systems.
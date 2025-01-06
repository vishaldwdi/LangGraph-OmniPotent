# langgraph-omnipotent

A powerful framework for building and orchestrating LangGraph applications, with a strong focus on Retrieval-Augmented Generation (RAG) agents.

## Overview
langgraph-omnipotent is a framework designed for building and orchestrating applications using LangGraph, enabling the creation of sophisticated agents for various tasks, including data enrichment and RAG-based question answering. It provides a unified graph structure to create complex workflows where specialized agents work together through defined steps such as gathering requirements, drafting solutions, performing checks, and undergoing critique. This allows for the development of agents that can perform open-ended research, retrieve relevant information, and produce structured results, enhancing language processing and reasoning capabilities. The framework includes specific components for indexing and retrieval, making it easier to build advanced RAG applications. The project is under active development, with ongoing efforts to expand model support and enhance retrieval mechanisms.

## Features
- Integrated Engineer Agent: Capabilities for code generation and modification.
- Enrichment Agent: Focuses on enhancing data and information by performing steps like web searching, information extraction, results organization, and validation to produce structured outputs.
- RAG Agents: Includes components for building Retrieval-Augmented Generation agents, with specific graphs for indexing (`index_graph`) and retrieval (`retrieval_graph`). The retrieval graph also incorporates a `researcher` subgraph for advanced query generation and document retrieval.
- Unified Graph Interface: Provides a cohesive structure for orchestrating agents and defining complex workflows.
- Shared Architecture: Promotes consistency and simplifies integration between agents.
- Centralized Configuration: Manages environment variables and shared functionalities for streamlined setup.
- Customizable Workflows: Allows users to define and tailor agent workflows to specific needs.
- Expanded Model Support: Includes support for Gemini, Groq, LM Studio, DeepSeek, and Ollama.
- Elasticsearch Integration: Enables document retrieval using Elasticsearch, with support for other vector stores like MongoDB Atlas and Pinecone.

## Key Features

*   **Agent Orchestration:** Define and manage complex workflows involving multiple LangGraph agents, with steps for requirement gathering, drafting, checks, and critique, enabling sophisticated agent interactions.
*   **Modular Design:**  Components are designed to be reusable and easily integrated.
*   **Flexible Configuration:** Configure agents and workflows through simple configuration files.
*   **Retrieval Integration:** Seamlessly integrate various retrieval mechanisms, including Elasticsearch, MongoDB Atlas, and Pinecone, for enhanced agent capabilities.
*   **Comprehensive Testing:** Includes a suite of unit and integration tests to ensure reliability.

## Getting Started

### Prerequisites

*   Python 3.8+
*   pip

### Installation

Clone the repository:

```bash
git clone <repository_url>
cd langgraph-omnipotent
```

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate  # On Windows
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

You can also try running this code locally with LangGraph Studio.

To explore the data enrichment capabilities, consider a research topic and desired extraction schema. For example, you might want to research:

"Top 5 chip providers for LLM Training"

And define a desired extraction schema like this:

```json
{
  "providers": [
    {
      "name": "string",
      "market_share": "string",
      "key_products": "list"
    }
  ]
}
```

To get started with the RAG agents, you'll need to set up a vector store. `langgraph-omnipotent` supports Elasticsearch, MongoDB Atlas, and Pinecone. Follow the instructions below for your preferred vector store.

#### Elasticsearch

Follow the instructions in the `langchain-ai/rag-research-agent-template` repository's README to set up Elasticsearch, either on Elastic Cloud or locally using Docker. Ensure you have the `ELASTICSEARCH_URL` and `ELASTICSEARCH_API_KEY` configured in your `.env` file.

#### MongoDB Atlas

Follow the instructions in the `langchain-ai/rag-research-agent-template` repository's README to set up a free MongoDB Atlas cluster and create a vector search index. Ensure you have the `MONGODB_URI` configured in your `.env` file.

#### Pinecone Serverless

Follow the instructions in the `langchain-ai/rag-research-agent-template` repository's README to sign up for a Pinecone account, create a serverless index, and obtain your API key and index name. Ensure you have the `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` configured in your `.env` file.

You'll also need to set up your preferred language and embedding models. The following environment variables can be configured in your `.env` file:

- `RESPONSE_MODEL`: Model for response generation (e.g., `anthropic/claude-3-5-sonnet-20240620`).
- `QUERY_MODEL`: Model for query generation (e.g., `anthropic/claude-3-haiku-20240307`).
- `EMBEDDING_MODEL`: Model for embeddings (e.g., `openai/text-embedding-3-small`).
- Respective API keys for the chosen models (e.g., `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `COHERE_API_KEY`).

### Configuration

Environment variables are managed in the `.env` file located in the root directory. Refer to the `.env.example` file for a comprehensive list of required variables.

Ensure you have the necessary API keys and vector store configurations set up in your `.env` file.

### How to Customize

You can customize and extend the functionality of `langgraph-omnipotent` in several ways:

- **Customize research targets:** When using the data enrichment agent, provide a custom JSON `extraction_schema` to gather different types of information.
- **Select a different model:** Configure the desired language model by specifying the provider and model name (e.g., `openai/gpt-4o-mini`) for response generation, query generation, and embeddings.
- **Adjust search parameters:** Fine-tune the retrieval process by modifying the `search_kwargs` in the relevant configuration files.
- **Customize the prompt:** Modify the default prompts used by the agents, located in the respective agent's directory (e.g., `src/retrieval_graph/prompts.py`).
- **Change the retriever:** Switch between different vector stores (Elasticsearch, MongoDB, Pinecone) by modifying the `retriever_provider` in the configuration and providing the necessary connection details.
- **Modify the embedding model:** Change the embedding model used for document indexing and query embedding by updating the `embedding_model` in the configuration.
- **Extend the graph:** Add new nodes or modify existing ones in the graph definitions (e.g., in `src/rag_agents/retrieval_graph/graph.py`) to introduce additional processing steps or decision points in the agent's workflow.
- **Add tools and API connections:** Extend agent capabilities by adding new Python functions as tools within the `tools.py` or similar files.

## Project Structure

*   `src/engineer-agent`: Contains the code for the engineer agent, responsible for tasks like code generation and modification.
*   `src/enrichment_agent`: Contains the code for the enrichment agent, focused on enhancing data or information by performing web research and structuring the results.
*   `src/rag_agents`: Includes implementations for Retrieval-Augmented Generation (RAG) agents, showcasing how to integrate retrieval mechanisms into agent workflows.
    *   `index_graph`: Contains the code for the indexing graph, responsible for indexing documents into the vector store.
    *   `retrieval_graph`: Contains the code for the retrieval graph, responsible for handling user queries, routing them, and generating responses based on retrieved documents.
        *   `researcher_graph`: Contains the code for the researcher subgraph, which generates search queries based on a research plan and retrieves relevant documents.
*   `src/shared_retrieval`: Provides reusable components for connecting to different retrieval systems like Elasticsearch, MongoDB Atlas, and Pinecone.
*   `src/shared_utils`: Contains utility functions used across the project, including model loading functionalities.
*   `unified_tests`: Holds integration tests that verify the interaction between different components.

## Usage

Detailed usage instructions and examples will be provided in the documentation.

To use the RAG agents, you can start by indexing documents using the `index_graph` in LangGraph Studio. Then, use the `retrieval_graph` to ask questions and receive answers based on the indexed documents.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Implement your changes.
4. Write tests to cover your changes.
5. Ensure all tests pass.
6. Submit a pull request.

## Credits

This framework is inspired by and builds upon the following open-source projects:

- [langgraph-engineer](https://github.com/hwchase17/langgraph-engineer)
- [data-enrichment](https://github.com/langchain-ai/data-enrichment) 
- [rag-research-agent-template](https://github.com/langchain-ai/rag-research-agent-template/tree/main)

This entire framework was developed in just 3 days with the assistance of AI coding models, demonstrating the power of human-AI collaboration in software development.

## License

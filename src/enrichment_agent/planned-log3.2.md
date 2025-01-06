# Planned Log 3.2

## Important Note

This document contains planned changes and roadmap items. Executed changes must be tracked in `/src/change-log.md`. Always reference both documents for complete project tracking.

## Documentation Policies

### Purpose and Scope

- Contains planned changes and roadmap items.
- Serves as a project planning and tracking tool.
- Guides development priorities and timelines.
- Complements `change-log.md` for complete project tracking.
- `planned-log3.md` should maintain its role as a forward-looking planning document with clear, incremental steps for future developers to follow.

### Writing Guidelines

1. **Entry Format**:
   - Phase/Feature: Clear section header.
   - Goal: Specific objective.
   - Steps: Detailed implementation plan.
   - Risks: Potential issues and mitigation.
   - Timeline: Estimated schedule.
   - Dependencies: Related components/tasks.
   - Audit Trail: Include date, author, changes made, and rationale.

2. **Content Standards**:
   - Be specific and actionable.
   - Include technical details and code snippets where relevant.
   - Document assumptions and constraints.
   - Note any prerequisites.
   - Maintain clear separation between planned and completed items.
   - Use clear language and define technical terms.
   - Include debugging strategies and common pitfalls.
   - Document best practices learned during troubleshooting.

3. **Organization**:
   - Group items by phase/feature.
   - Maintain logical flow and continuity with previous entries.
   - Use clear section headers and bullet points.
   - Include cross-references to related `change-log.md` entries.
   - Categorize issues by severity and module affected.

### Update Procedures

1. Add new items during planning phases.
2. Update existing items as plans evolve.
3. Mark completed items with reference to `change-log.md`.
4. Maintain version history of changes.
5. Archive completed phases for historical reference.

### Review Process

1. Initial review by proposing developer.
2. Technical review by team with focus on:
   - Logical flow and continuity.
   - Completeness of audit trail.
   - Effectiveness of documented solutions.
3. Peer review for clarity and correctness.
4. Final approval by project lead.
5. Periodic reviews to ensure alignment with project goals.
6. Compliance review for any regulatory requirements.

### Version Control

1. Commit changes with clear messages.
2. Include `planned-log.md` updates in planning commits.
3. Use pull requests for documentation changes.
4. Maintain change history through Git commits.

### Maintenance

1. Project lead oversees documentation quality.
2. All developers responsible for their sections.
3. Monthly reviews for accuracy and relevance.
4. Quarterly audits to ensure completeness.
5. Annual review of overall roadmap alignment.

## Summary of Phases 1-8 -> Look root/planned-log.md if details are required

### Phase 1: Project Name Change

**Goal:** Rename the project from `engineer_agent` to `langgraph-omnipotent`.

**Key Steps:** Update configuration files (`pyproject.toml`, `langgraph.json`, `.env.example`, `README.md`), rename the main directory, update import statements, and update documentation.

### Phase 2: Code Integration and Unification

**Goal:** Integrate the `enrichment_agent` codebase into the `langgraph-omnipotent` project and unify the project structure.

**Key Steps:** Standardize import paths, plan code integration, update configuration mapping, strategize JSON configuration, manage dependencies, and implement testing.

### Phase 3: Backend Logic for Agent Selection and Configuration

**Goal:** Implement backend logic to select and run either the `engineer_agent` or `enrichment_agent`, and handle configurable options.

**Key Steps:** Implement agent selection logic based on a configuration setting (e.g., an environment variable).

### Phase 4: Sharing Architecture

**Goal:** Share functionalities from `src/rag_agents/shared/retrieval.py` and `src/rag_agents/shared/utils.py` at the `/src/` level.

**Key Steps:** Create `src/shared_retrieval/` and `src/shared_utils/` directories, move relevant functions, create base classes and factories for retrievers, and update import statements.

### Phase 5: Centralizing Environment Variables and Utilizing Shared Functionalities

**Goal:** Centralize environment variables in the root `.env` file and outline how other agents will utilize the shared functionalities.

**Key Steps:** Consolidate environment variables from agent-specific `.env.example` files into the root `.env` file, update code to fetch variables from the root `.env`, and detail how the engineer and enrichment agents will use the shared retrieval and utility functionalities.

### Phase 6: Refinement and Documentation

**Goal:** Ensure the `langgraph-omnipotent` project is well-documented, tested, and ready for use.

**Key Steps:** Update documentation, perform comprehensive testing, and clean up and optimize the code.

### Phase 7: Expanding Model Support and Configuring Retrievers

**Goal:** Expand model support to include Gemini, Groq, LM Studio, DeepSeek, and Ollama, and ensure the correct configuration of the existing Elasticsearch retriever.

**Key Steps:** Install necessary libraries, update `load_chat_model` in `src/shared_utils/model_utils.py`, implement Elasticsearch retrieval logic in `src/shared_retrieval/elasticsearch_retriever.py`, update configurations, and standardize environment variable usage.

### Phase 8: Detailed Model and Retriever Integration

**Goal:** Provide a detailed plan for integrating each new model and ensuring the correct functioning of the Elasticsearch retriever.

**Key Steps:** Define specific integration steps for each new model in `src/shared_utils/model_utils.py`, detail Elasticsearch retrieval logic implementation in `src/shared_retrieval/elasticsearch_retriever.py`, and outline testing requirements for both model loading and Elasticsearch retrieval.

## Phase 9.2: Agentic Graph Improvements

### Section 2: Enrichment Agent Graph Improvements

**Goal:** To refine the enrichment agent graph for better performance and functionality, focusing on explicit tool use, robust error handling, and data validation, while also incorporating configuration management, security, scalability, interoperability, monitoring, documentation, versioning, and user feedback.

**Target Graph Structure:**

```
CREATE
  (enrichment_start:Node {name: '_start_'}),

  // State Node
  (enrichment_state:Node {name: 'agent_state', current: 'initial'}),

  // --- RAG Functionality ---
  (enrichment_queryKnowledgeBase:Node {name: 'query_knowledge_base'}),
  (enrichment_queryKnowledgeBase)-[:NEXT]->(enrichment_state {current: 'querying_kb'}),
  (enrichment_queryKnowledgeBase)-[:COMPLETES]->(enrichment_getContext), // Directly to next step

  // Context Retrieval (Now potentially using RAG result)
  (enrichment_getContext:Node {name: 'get_context'}),
  (enrichment_getContext)-[:NEXT]->(enrichment_state {current: 'getting_context'}),

  // Asynchronous Tool Use
  (enrichment_requestTool:Node {name: 'request_tool'}),
  (enrichment_getContext)-[:NEXT]->(enrichment_requestTool),
  (enrichment_requestTool)-[:NEXT]->(enrichment_state {current: 'waiting_for_tool'}),
  (enrichment_requestTool)-[:ASYNC_COMPLETES_WITH_RESULT]->(enrichment_validateData), // Direct to validation on success
  (enrichment_requestTool)-[:ASYNC_COMPLETES_WITH_ERROR]->(enrichment_state {current: 'tool_error'}),
  (enrichment_requestTool)-[:ASYNC_COMPLETES_WITH_ERROR]->(enrichment_generateResponse), // Error handling

  // Data Validation
  (enrichment_validateData:Node {name: 'validate_data'}),
  (enrichment_validateData)-[:NEXT]->(enrichment_state {current: 'validating_data'}),
  (enrichment_validateData)-[:ON_SUCCESS]->(enrichment_generateEnrichment),
  (enrichment_validateData)-[:ON_FAILURE]->(enrichment_state {current: 'data_validation_failed'}),
  (enrichment_validateData)-[:ON_FAILURE]->(enrichment_generateResponse), // Error handling

  // Enrichment Generation (Potentially Asynchronous)
  (enrichment_generateEnrichment:Node {name: 'generate_enrichment'}),
  (enrichment_generateEnrichment)-[:NEXT]->(enrichment_state {current: 'enriching_data'}),
  (enrichment_generateEnrichment)-[:ASYNC_COMPLETES_WITH_RESULT]->(enrichment_generateResponse), // Direct to response on success
  (enrichment_generateEnrichment)-[:ASYNC_COMPLETES_WITH_ERROR]->(enrichment_state {current: 'enrichment_failed'}),
  (enrichment_generateEnrichment)-[:ASYNC_COMPLETES_WITH_ERROR]->(enrichment_generateResponse), // Error handling

  // Response Generation
  (enrichment_generateResponse:Node {name: 'generate_response'}),
  (enrichment_generateResponse)-[:NEXT]->(enrichment_state {current: 'generating_response'}),
  (enrichment_generateResponse)-[:NEXT]->(enrichment_sendMessage), // Move to next step

  // Interoperability with Other Agents
  (enrichment_sendMessage:Node {name: 'send_message'}),
  (enrichment_sendMessage)-[:NEXT]->(enrichment_state {current: 'sending_message'}),
  (enrichment_sendMessage)-[:COMPLETES]->(enrichment_state {current: 'idle'}), // End of successful flow

  (enrichment_receiveMessage:Node {name: 'receive_message'}),
  (enrichment_receiveMessage)-[:NEXT]->(enrichment_state {current: 'receiving_message'}),
  (enrichment_receiveMessage)-[:COMPLETES]->(enrichment_getContext), // Received message influences context

  // User Feedback Mechanism
  (enrichment_getFeedback:Node {name: 'get_feedback'}),
  (enrichment_generateResponse)-[:PROVIDES_FEEDBACK]->(enrichment_getFeedback),

  // Configuration (Conceptual)
  (enrichment_config:Node {name: 'configuration'}),
  (enrichment_start)-[:CONFIGURED_BY]->(enrichment_config),
  (enrichment_queryKnowledgeBase)-[:CONFIGURED_BY]->(enrichment_config),
  (enrichment_getContext)-[:CONFIGURED_BY]->(enrichment_config),
  (enrichment_requestTool)-[:CONFIGURED_BY]->(enrichment_config),
  (enrichment_validateData)-[:CONFIGURED_BY]->(enrichment_config),
  (enrichment_generateEnrichment)-[:CONFIGURED_BY]->(enrichment_config),
  (enrichment_generateResponse)-[:CONFIGURED_BY]->(enrichment_config),
  (enrichment_sendMessage)-[:CONFIGURED_BY]->(enrichment_config),
  (enrichment_receiveMessage)-[:CONFIGURED_BY]->(enrichment_config),

  // Monitoring (Conceptual)
  (enrichment_monitoring:Node {name: 'monitoring'}),
  (enrichment_queryKnowledgeBase)-[:MONITORED_BY]->(enrichment_monitoring),
  (enrichment_getContext)-[:MONITORED_BY]->(enrichment_monitoring),
  (enrichment_requestTool)-[:MONITORED_BY]->(enrichment_monitoring),
  (enrichment_validateData)-[:MONITORED_BY]->(enrichment_monitoring),
  (enrichment_generateEnrichment)-[:MONITORED_BY]->(enrichment_monitoring),
  (enrichment_generateResponse)-[:MONITORED_BY]->(enrichment_monitoring),
  (enrichment_sendMessage)-[:MONITORED_BY]->(enrichment_monitoring),
  (enrichment_receiveMessage)-[:MONITORED_BY]->(enrichment_monitoring),

  // Initial State Transition
  (enrichment_start)-[:NEXT]->(enrichment_queryKnowledgeBase),
  (enrichment_start)-[:TRANSITION_TO_STATE]->(enrichment_state {current: 'initial'})
```

### Section 2: Enrichment Agent Graph Improvements

**Goal:** To refine the enrichment agent graph for better performance and functionality, focusing on explicit tool use, robust error handling, and data validation, while also incorporating configuration management, security, scalability, interoperability, monitoring, documentation, versioning, and user feedback.

**Project File Structure:**

```
src/
├── enrichment_agent/
│   ├── graph.py  # Defines the graph structure and node logic
│   ├── ...       # Other enrichment agent related files
├── shared_retrieval/
│   ├── ...       # Shared retrieval functionalities
├── shared_utils/
│   ├── ...       # Shared utility functions
└── ...           # Other project directories and files
```

**Steps:**

1. **Start Node (`enrichment_start`):**
   - **Goal:** To initiate the enrichment process.
   - **Steps:**
     - Define the `enrichment_start` node in `src/enrichment_agent/graph.py`.
     - Implement logic for the `enrichment_start` node to transition to the `enrichment_queryKnowledgeBase` node.
     - Implement logic for the `enrichment_start` node to transition to the `enrichment_state` node and set its `current` property to 'initial'.
   - **Risks:** No clear start can halt the process.
   - **Dependencies:** `src/enrichment_agent/graph.py`, `enrichment_queryKnowledgeBase` node, `enrichment_state` node.

2. **Agent State Node (`enrichment_state`):**
    - **Goal:** To maintain the current state of the enrichment agent.
    - **Steps:**
        - Define the `enrichment_state` node in `src/enrichment_agent/graph.py` with a `current` property.
        - Implement logic in the `enrichment_queryKnowledgeBase` node to transition to `enrichment_state` and set `current` to 'querying_kb'.
        - Implement logic in the `enrichment_getContext` node to transition to `enrichment_state` and set `current` to 'getting_context'.
        - Implement logic in the `enrichment_requestTool` node to transition to `enrichment_state` and set `current` to 'waiting_for_tool'.
        - Implement logic in the `enrichment_requestTool` node to transition to `enrichment_state` and set `current` to 'tool_error' on error.
        - Implement logic in the `enrichment_validateData` node to transition to `enrichment_state` and set `current` to 'validating_data'.
        - Implement logic in the `enrichment_validateData` node to transition to `enrichment_state` and set `current` to 'data_validation_failed' on failure.
        - Implement logic in the `enrichment_generateEnrichment` node to transition to `enrichment_state` and set `current` to 'enriching_data'.
        - Implement logic in the `enrichment_generateEnrichment` node to transition to `enrichment_state` and set `current` to 'enrichment_failed' on error.
        - Implement logic in the `enrichment_generateResponse` node to transition to `enrichment_state` and set `current` to 'generating_response'.
        - Implement logic in the `enrichment_sendMessage` node to transition to `enrichment_state` and set `current` to 'sending_message'.
        - Implement logic in the `enrichment_sendMessage` node to transition to `enrichment_state` and set `current` to 'idle' on completion.
        - Implement logic in the `enrichment_receiveMessage` node to transition to `enrichment_state` and set `current` to 'receiving_message'.
    - **Risks:** Inaccurate state tracking can lead to incorrect behavior.
    - **Dependencies:** All nodes that transition and affect the agent's state.

3. **Query Knowledge Base Node (`enrichment_queryKnowledgeBase`):**
   - **Goal:** To query the knowledge base for relevant information.
   - **Steps:**
     - Define the `enrichment_queryKnowledgeBase` node in `src/enrichment_agent/graph.py`.
     - Implement logic to interact with the knowledge base using shared retrieval functionalities (`src/shared_retrieval/`).
     - Implement a transition to the `enrichment_state` node, setting the `current` property to 'querying_kb'.
     - Implement a transition to the `enrichment_getContext` node upon completion.
   - **Risks:** Failure to retrieve relevant information.
   - **Dependencies:** `src/shared_retrieval/`, `enrichment_getContext` node, `enrichment_state` node.

4. **Get Context Node (`enrichment_getContext`):**
   - **Goal:** To retrieve the necessary context for enrichment, potentially using RAG results.
   - **Steps:**
     - Define the `enrichment_getContext` node in `src/enrichment_agent/graph.py`.
     - Implement logic to retrieve context, potentially utilizing the results from `enrichment_queryKnowledgeBase`.
     - Implement a transition to the `enrichment_state` node, setting the `current` property to 'getting_context'.
     - Implement a transition to the `enrichment_requestTool` node.
   - **Risks:** Insufficient context for enrichment.
   - **Dependencies:** `enrichment_queryKnowledgeBase` node, `enrichment_requestTool` node, `enrichment_state` node.

5. **Request Tool Node (`enrichment_requestTool`):**
   - **Goal:** To request the use of an external tool.
   - **Steps:**
     - Define the `enrichment_requestTool` node in `src/enrichment_agent/graph.py`.
     - Implement logic to identify and request the appropriate tool based on the context.
     - Implement a transition to the `enrichment_state` node, setting the `current` property to 'waiting_for_tool'.
     - Implement an asynchronous transition to the `enrichment_validateData` node upon successful tool execution.
     - Implement asynchronous transitions to the `enrichment_state` node (setting `current` to 'tool_error') and the `enrichment_generateResponse` node upon tool execution error.
   - **Risks:** Failure to request the correct tool or tool unavailability.
   - **Dependencies:** `enrichment_getContext` node, `enrichment_validateData` node, `enrichment_state` node, `enrichment_generateResponse` node.

6. **Validate Data Node (`enrichment_validateData`):**
    - **Goal:** To validate the data obtained from the tool.
    - **Steps:**
        - Define the `enrichment_validateData` node in `src/enrichment_agent/graph.py`.
        - Implement logic to validate the data against a predefined schema or criteria.
        - Implement a transition to the `enrichment_state` node, setting the `current` property to 'validating_data'.
        - Implement a transition to the `enrichment_generateEnrichment` node on successful validation.
        - Implement transitions to the `enrichment_state` node (setting `current` to 'data_validation_failed') and the `enrichment_generateResponse` node on validation failure.
    - **Risks:** Incorrect data validation leading to errors.
    - **Dependencies:** `enrichment_requestTool` node, `enrichment_generateEnrichment` node, `enrichment_generateResponse` node, `enrichment_state` node.

7. **Generate Enrichment Node (`enrichment_generateEnrichment`):**
    - **Goal:** To generate the final enriched data.
    - **Steps:**
        - Define the `enrichment_generateEnrichment` node in `src/enrichment_agent/graph.py`.
        - Implement logic to generate enriched data based on the validated data.
        - Implement a transition to the `enrichment_state` node, setting the `current` property to 'enriching_data'.
        - Implement an asynchronous transition to the `enrichment_generateResponse` node upon successful enrichment.
        - Implement asynchronous transitions to the `enrichment_state` node (setting `current` to 'enrichment_failed') and the `enrichment_generateResponse` node on enrichment error.
    - **Risks:** Errors during the enrichment generation process.
    - **Dependencies:** `enrichment_validateData` node, `enrichment_generateResponse` node, `enrichment_state` node.

8. **Generate Response Node (`enrichment_generateResponse`):**
    - **Goal:** To generate a response to the user.
    - **Steps:**
        - Define the `enrichment_generateResponse` node in `src/enrichment_agent/graph.py`.
        - Implement logic to create a user-friendly response based on the outcome of the enrichment process.
        - Implement a transition to the `enrichment_state` node, setting the `current` property to 'generating_response'.
        - Implement a transition to the `enrichment_sendMessage` node.
    - **Risks:** Generating unclear or unhelpful responses.
    - **Dependencies:** `enrichment_validateData` node, `enrichment_requestTool` node, `enrichment_generateEnrichment` node, `enrichment_sendMessage` node, `enrichment_state` node.

9. **Send Message Node (`enrichment_sendMessage`):**
    - **Goal:** To send the generated response message.
    - **Steps:**
        - Define the `enrichment_sendMessage` node in `src/enrichment_agent/graph.py`.
        - Implement logic to send the response message to the user or another agent.
        - Implement a transition to the `enrichment_state` node, setting the `current` property to 'sending_message'.
        - Implement a transition to the `enrichment_state` node, setting the `current` property to 'idle' upon completion.
    - **Risks:** Failure to send the message.
    - **Dependencies:** `enrichment_generateResponse` node, `enrichment_state` node.

10. **Receive Message Node (`enrichment_receiveMessage`):**
    - **Goal:** To handle receiving messages from other agents.
    - **Steps:**
        - Define the `enrichment_receiveMessage` node in `src/enrichment_agent/graph.py`.
        - Implement logic to listen for and receive messages from other agents.
        - Implement a transition to the `enrichment_state` node, setting the `current` property to 'receiving_message'.
        - Implement a transition to the `enrichment_getContext` node upon receiving a message.
    - **Risks:** Failure to receive messages.
    - **Dependencies:** `enrichment_getContext` node, `enrichment_state` node.

11. **Get Feedback Node (`enrichment_getFeedback`):**
    - **Goal:** To obtain user feedback on the response.
    - **Steps:**
        - Define the `enrichment_getFeedback` node in `src/enrichment_agent/graph.py`.
        - Implement logic to present the response to the user and solicit feedback.
    - **Risks:** Failure to gather user feedback.
    - **Dependencies:** `enrichment_generateResponse` node.

12. **Configuration Node (`enrichment_config`):**
    - **Goal:** To manage the configuration of the enrichment process.
    - **Steps:**
        - Define the conceptual `enrichment_config` node.
        - Implement logic across the following nodes to utilize configuration parameters: `enrichment_start`, `enrichment_queryKnowledgeBase`, `enrichment_getContext`, `enrichment_requestTool`, `enrichment_validateData`, `enrichment_generateEnrichment`, `enrichment_generateResponse`, `enrichment_sendMessage`, `enrichment_receiveMessage`.
    - **Risks:** Incorrect configuration leading to errors.
    - **Dependencies:** `enrichment_start`, `enrichment_queryKnowledgeBase`, `enrichment_getContext`, `enrichment_requestTool`, `enrichment_validateData`, `enrichment_generateEnrichment`, `enrichment_generateResponse`, `enrichment_sendMessage`, `enrichment_receiveMessage` nodes.

13. **Monitoring Node (`enrichment_monitoring`):**
    - **Goal:** To monitor the enrichment process for performance and errors.
    - **Steps:**
        - Define the conceptual `enrichment_monitoring` node.
        - Implement logging and monitoring mechanisms within the following nodes: `enrichment_queryKnowledgeBase`, `enrichment_getContext`, `enrichment_requestTool`, `enrichment_validateData`, `enrichment_generateEnrichment`, `enrichment_generateResponse`, `enrichment_sendMessage`, `enrichment_receiveMessage`.
    - **Risks:** Inadequate monitoring leading to undetected issues.
    - **Dependencies:** `enrichment_queryKnowledgeBase`, `enrichment_getContext`, `enrichment_requestTool`, `enrichment_validateData`, `enrichment_generateEnrichment`, `enrichment_generateResponse`, `enrichment_sendMessage`, `enrichment_receiveMessage` nodes.

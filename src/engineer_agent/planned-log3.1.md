# Planned Log 3.1

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

## Phase 9.1: Agentic Graph Improvements

### Section 1: Engineer Agent Graph Improvements

**Goal:** To refine the engineer agent graph to achieve software engineering objectives with excellence, focusing on code quality, error detection, and workflow efficiency.

**Target Graph Structure:**

```
// Consolidated and Robust Engineer Agent Workflow with Explicit Error Handling

// Shared Start Node
CREATE (:Start {name: "_start_", description: "Initiates the software engineering task"});

// Initial State Node
CREATE (:State {name: "Initial", description: "Agent is ready to begin"});

// Connect Start to Initial State
CREATE (:Start {name: "_start_"})-[:TRANSITION_TO]->(:State {name: "Initial"});

// Gather Requirements Stage
CREATE (:Task {name: "gather_requirements", objective: "Understand the task requirements and constraints", state_change: "RequirementsGathered"});
CREATE (:State {name: "RequirementsGathered", description: "Task requirements have been collected"});
CREATE (:State {name: "AwaitingTaskTypeDecision", description: "Ready to decide between answer or code generation"});
CREATE (:State {name: "RequirementsError", description: "Error encountered while gathering requirements"}); // Error State

CREATE (:State {name: "Initial"})-[:NEXT]->(:Task {name: "gather_requirements"});
CREATE (:Task {name: "gather_requirements"})-[:ON_SUCCESS]->(:State {name: "RequirementsGathered"});
CREATE (:Task {name: "gather_requirements"})-[:ON_FAILURE]->(:State {name: "RequirementsError"}); // Error Transition
CREATE (:State {name: "RequirementsGathered"})-[:NEXT]->(:State {name: "AwaitingTaskTypeDecision"});
CREATE (:State {name: "RequirementsError"})-[:NEXT]->(:Task {name: "handle_requirements_error"}); // Error Handling Task

CREATE (:Task {name: "handle_requirements_error", objective: "Attempt to recover from requirements error or abort"});
CREATE (:Task {name: "handle_requirements_error"})-[:NEXT]->(:End {name: "workflow_aborted", reason: "Error in gathering requirements"});

// Decision Point: Answer or Code Generation
CREATE (:Decision {name: "decide_task_type", criteria: "Analyze requirements to determine if an answer or code is needed"});

CREATE (:State {name: "AwaitingTaskTypeDecision"})-[:NEXT]->(:Decision {name: "decide_task_type"});

// --- Subgraph: Answer Drafting ---
CREATE (:Subgraph {name: "AnswerDrafting", description: "Workflow for generating a text-based answer"});
CREATE (:Task {name: "draft_answer", objective: "Generate an initial response or solution", state_change: "AnswerDrafted"});
CREATE (:State {name: "AnswerDrafted", description: "Initial answer has been generated"});
CREATE (:Stage {name: "check_answer", objective: "Review the drafted answer for accuracy and completeness", state_change: "AnswerChecked"});
CREATE (:State {name: "AnswerChecked", description: "Answer has been reviewed"});
CREATE (:Stage {name: "critique_answer", objective: "Provide feedback and identify areas for improvement"});

CREATE (:Decision {name: "answer_satisfactory", criteria: "Is the answer accurate, complete, and meets requirements?"});
CREATE (:End {name: "answer_ready", description: "Answer drafting complete"});
CREATE (:State {name: "AnswerDraftingError", description: "An error occurred during answer drafting"});

CREATE (:Decision {name: "decide_task_type"})-[:IF_ANSWER {condition: "Requirements suggest a non-code solution"}]->(:Subgraph {name: "AnswerDrafting"});

CREATE (:Subgraph {name: "AnswerDrafting"})-[:STARTS_WITH]->(:Task {name: "draft_answer"});
CREATE (:Task {name: "draft_answer"})-[:ON_SUCCESS]->(:State {name: "AnswerDrafted"});
CREATE (:Task {name: "draft_answer"})-[:ON_FAILURE]->(:State {name: "AnswerDraftingError"}); // Error Transition
CREATE (:State {name: "AnswerDrafted"})-[:NEXT]->(:Stage {name: "check_answer"});
CREATE (:Stage {name: "check_answer"})-[:ON_SUCCESS]->(:State {name: "AnswerChecked"});
CREATE (:Stage {name: "check_answer"})-[:ON_FAILURE]->(:State {name: "AnswerDraftingError"}); // Error Transition
CREATE (:State {name: "AnswerChecked"})-[:NEXT]->(:Stage {name: "critique_answer"});
CREATE (:Stage {name: "critique_answer"})-[:NEXT]->(:Decision {name: "answer_satisfactory"});
CREATE (:Decision {name: "answer_satisfactory"})-[:YES]->(:End {name: "answer_ready"});
CREATE (:Decision {name: "answer_satisfactory"})-[:NO]->(:Task {name: "draft_answer"}); // Loop back for revisions
CREATE (:State {name: "AnswerDraftingError"})-[:NEXT]->(:Task {name: "handle_answer_error"}); // Error Handling Task

CREATE (:Task {name: "handle_answer_error", objective: "Attempt to recover from answer drafting error or escalate"});
CREATE (:Task {name: "handle_answer_error"})-[:NEXT]->(:End {name: "workflow_completed"}); // Example: Simple exit after handling

// --- Subgraph: Code Development ---
CREATE (:Subgraph {name: "CodeDevelopment", description: "Workflow for generating and refining code"});
CREATE (:Task {name: "draft_code", objective: "Write the initial code implementation", state_change: "CodeDrafted"});
CREATE (:State {name: "CodeDrafted", description: "Initial code has been written"});
CREATE (:Stage {name: "critique_code", objective: "Conduct code review for quality and standards", state_change: "CodeCritiqued"});
CREATE (:State {name: "CodeCritiqued", description: "Code review complete"});
CREATE (:Stage {name: "check_code", objective: "Execute automated tests and static analysis", state_change: "CodeChecked"});
CREATE (:State {name: "CodeChecked", description: "Automated checks complete"});
CREATE (:Task {name: "respond_to_user", objective: "Deliver the code or feedback"});

CREATE (:Decision {name: "code_acceptable", criteria: "Does the code meet quality standards and pass checks?"});
CREATE (:End {name: "code_delivered", description: "Code development complete and delivered"});
CREATE (:State {name: "CodeDevelopmentError", description: "An error occurred during code development"});

CREATE (:Decision {name: "decide_task_type"})-[:IF_CODE {condition: "Requirements suggest a code-based solution"}]->(:Subgraph {name: "CodeDevelopment"});

CREATE (:Subgraph {name: "CodeDevelopment"})-[:STARTS_WITH]->(:Task {name: "draft_code"});
CREATE (:Task {name: "draft_code"})-[:ON_SUCCESS]->(:State {name: "CodeDrafted"});
CREATE (:Task {name: "draft_code"})-[:ON_FAILURE]->(:State {name: "CodeDevelopmentError"}); // Error Transition
CREATE (:State {name: "CodeDrafted"})-[:NEXT]->(:Stage {name: "critique_code"});
CREATE (:Stage {name: "critique_code"})-[:ON_SUCCESS]->(:State {name: "CodeCritiqued"});
CREATE (:Stage {name: "critique_code"})-[:ON_FAILURE]->(:State {name: "CodeDevelopmentError"}); // Error Transition
CREATE (:State {name: "CodeCritiqued"})-[:NEXT]->(:Stage {name: "check_code"});
CREATE (:Stage {name: "check_code"})-[:ON_SUCCESS]->(:State {name: "CodeChecked"});
CREATE (:Stage {name: "check_code"})-[:ON_FAILURE]->(:State {name: "CodeDevelopmentError"}); // Error Transition
CREATE (:State {name: "CodeChecked"})-[:NEXT]->(:Decision {name: "code_acceptable"});
CREATE (:Decision {name: "code_acceptable"})-[:YES]->(:Task {name: "respond_to_user"});
CREATE (:Task {name: "respond_to_user"})-[:NEXT]->(:End {name: "code_delivered"});
CREATE (:Decision {name: "code_acceptable"})-[:NO]->(:Task {name: "draft_code"}); // Loop back for code refinement
CREATE (:State {name: "CodeDevelopmentError"})-[:NEXT]->(:Task {name: "handle_code_error"}); // Error Handling Task

CREATE (:Task {name: "handle_code_error", objective: "Attempt to recover from code development error or escalate"});
CREATE (:Task {name: "handle_code_error"})-[:NEXT]->(:End {name: "workflow_completed"}); // Example: Simple exit after handling

// --- Connecting End Points and Potential Unified Final State ---
CREATE (:End {name: "workflow_completed", description: "The overall engineer agent workflow has completed"});
CREATE (:End {name: "answer_ready"})-[:NEXT]->(:End {name: "workflow_completed"});
CREATE (:End {name: "code_delivered"})-[:NEXT]->(:End {name: "workflow_completed"});
CREATE (:End {name: "workflow_aborted", description: "The workflow was terminated due to an error", reason: ""}); // Added general abort
```

### Steps:

1. **Implement Granular Critique and Automated Analysis:**
    -   **Goal:** Integrate static analysis tools (`pylint`, `flake8`) into the agent's workflow to automatically identify potential issues in the drafted code. Enhance the `check_code` node to provide specific error information, improving code quality and error detection.
    -   **Implementation Details:**
        -   **Create `automated_critique` Node:** Implement a new node named `automated_critique` within the `src/engineer_agent/agent.py` file. This node will be positioned in the graph flow following the `check_code` node. The transition from `check_code` to `automated_critique` will occur when `check_code` identifies semantic errors.
        -   **Static Analysis Execution:** Within the `automated_critique` node, the system will execute static analysis using `pylint` and `flake8`.
            -   **Code Access:** The `automated_critique` node will access the generated code from the `AgentState`. The code will be saved to a temporary file in `/tmp/engineer_agent_temp/`, ensuring each file has a unique name to prevent conflicts.
            -   **Pylint Configuration:** Execute `pylint` with the command `pylint <temporary_code_file_path>`, utilizing a `.pylintrc` file located at the project root for configuration.
            -   **Flake8 Configuration:** Execute `flake8` with the command `flake8 --max-line-length=120 --isolated --select=C,D,E,F,I,W <temporary_code_file_path>`.
            -   **Output Capture:** The standard output and standard error from both `pylint` and `flake8` will be captured for analysis.
            -   **Error Parsing:** The output from `pylint` and `flake8` will be parsed to pinpoint specific errors and warnings.
        -   **Enhance `check_code` Node:** Modify the `check_code` node in `src/engineer_agent/check.py` to classify detected errors.
            -   **Syntax Errors:** If parsing the code with `ast.parse()` results in a `SyntaxError`, the `check_code` node will signal a transition back to the `draft_code` node.
            -   **Semantic Errors:** If `pylint` or `flake8` report errors (excluding warnings), the `check_code` node will signal a transition to the `automated_critique` node. Specific error messages and codes will be stored in the `AgentState`.
            -   **Logical Errors:** This category is a placeholder for future implementation, potentially involving unit tests or other validation methods.
        -   **Output to State:** Update the `AgentState` in `src/engineer_agent/state.py` to include `check_output` (containing error classifications) and `static_analysis_output` (containing raw output from `pylint` and `flake8`).
2. **Enhance Decision Making in `decide_next_step`:**
    -   **Goal:** Refine the decision-making process within the `decide_next_step` node in `src/engineer_agent/agent.py` to intelligently determine the subsequent workflow action, focusing on error handling and loop prevention.
    -   **Implementation Details:**
        -   **Create `decide_next_step` Node:** Implement a new node named `decide_next_step` in `src/engineer_agent/agent.py`. This node will evaluate the current `AgentState` to determine the next step.
        -   **Track Iterations:** Introduce an `iteration_count` key in the `AgentState` within `src/engineer_agent/state.py`. This counter will increment each time the graph returns to a drafting or critique node. A `max_iterations` limit (e.g., 5), defined in `EngineerAgentConfiguration` in `src/engineer_agent/config.py`, will be enforced to prevent infinite loops, redirecting to `respond_to_user` if exceeded.
        -   **Consider Error Severity:** The `decide_next_step` node will analyze error classifications from `check_code` and outputs from `automated_critique`.
            -   Syntax errors identified by `check_code` will direct the flow back to `draft_code`.
            -   Semantic errors (identified by "error" in `pylint` or `flake8` output) or issues found by `automated_critique` will also direct the flow to `draft_code`.
            -   Minor warnings from `check_code` (e.g., style issues from `flake8`) will allow progression to `llm_critique`. Severe warnings (non-style `flake8` or any `pylint` warnings) will cause `check_code` to directly loop back to `draft_code`, bypassing `decide_next_step`.
        -   **User Clarification:** If the agent loops three consecutive times with the same error type, `decide_next_step` will transition to a new `ask_clarification` node, prompting the user for more information before moving to `gather_requirements` or `draft_code` as needed.
3. **More Detailed State Management:**
    -   **Goal:** Expand the `AgentState` in `src/engineer_agent/state.py` to maintain comprehensive information throughout the engineering process.
    -   **Implementation Details:** Add the following keys to `AgentState`: `check_output` (dictionary with raw output from `check_code` and error classifications), `critique_feedback` (feedback from `llm_critique`), `iteration_count` (number of iterations), and `static_analysis_output` (dictionary with raw output from `pylint` and `flake8`).
4. **Tool Utilization in Critique and Check:**
    -   **Goal:** Enable the `CritiqueCode` and `CheckCode` classes to leverage available tools for enhanced functionality.
    -   **Implementation Details:**
        -   **`CheckCode`:** Modify the `CheckCode` class in `src/engineer_agent/check.py` to utilize the `read_file` tool to access the generated code. The temporary file path from `AgentState.temp_file_path` will be used to read the code for analysis.
        -   **`CritiqueCode`:** Modify the `CritiqueCode` class in `src/engineer_agent/critique.py` to potentially use tools like `read_file` to access related files or documentation, determined by the context of the code review.
5. **Improved Failure Handling:**
    -   **Goal:** Enhance the robustness of the workflow by implementing explicit handling for different failure types within the `check_code` stage.
    -   **Implementation Details:** The `check_code` node will return a specific output indicating the error type (e.g., `{"error_type": "syntax"}`) after classifying it. The graph definition in `src/engineer_agent/agent.py` will use `add_conditional_edges` to direct transitions based on these error types (e.g., `check_code --(fails - syntax error)--> draft_code`, `check_code --(fails - semantic error)--> automated_critique`). The conditions in `decide_next_step` will align with these specific error types. Logical errors will initially follow the same path as semantic errors.
6. **Communication and Transparency:**
    -   **Goal:** Improve communication and transparency by providing more detailed feedback to the user during the engineering process.
    -   **Implementation Details:**
        -   **Logging:** Implement logging within agent nodes using the `logging` module to record key decisions, errors, and tool outputs, stored in a timestamped log file (e.g., `engineer_agent.log`).
        -   **Detailed Feedback Node:** Add a `provide_feedback` node in `src/engineer_agent/agent.py`, positioned after `llm_critique`. The flow will move from `llm_critique` to `provide_feedback`, where a summary of recent steps and findings will be formatted for the user, before transitioning to `respond_to_user`.
        -   **Enhance `respond_to_user`:** Modify the `respond_to_user` node in `src/engineer_agent/agent.py` to include more information from `AgentState`, such as iteration count, warnings, errors, and the reasoning behind the final code.

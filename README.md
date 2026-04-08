# Email Triage OpenEnv

## Environment Overview and Motivation
This environment presents a real-world scenario: managing a professional email inbox. Agents are tasked with parsing unread emails and deciding whether to mark them as read, archive them, or reply to them based on context. This evaluates an LLM's capacity for context evaluation and deterministic state changes in an API-driven environment.

## Action and Observation Spaces
*   **Observation Space**: Typed via `Obs` Pydantic model. Contains an array of email objects (subject, text, and status) and the current active index.
*   **Action Space**: Typed via `Act` Pydantic model. Requires an action string (`rd` for read, `arc` for archive, `rep` for reply), the target integer index, and an optional text field for replies.

## Tasks and Difficulties
1.  **Task 1 (Easy)**: A single greeting email. Tests basic syntax execution.
2.  **Task 2 (Medium)**: Two emails combining an invoice and a spam message. Introduces decision-making on archiving vs responding.
3.  **Task 3 (Hard)**: Three emails containing bugs, social inquiries, and critical system errors. Requires prioritization within the action limit.

## Grader and Reward Function
The environment evaluates trajectories sequentially.
*   **Step Rewards**: Incrementally granted based on appropriate actions (e.g., replying yields more reward than simply reading). Invalid actions or out-of-bound indices yield penalties (-0.1).
*   **Task Grader**: Handled inside `info["score"]` at task termination. Evaluates the ratio of successfully processed emails over total initial unread emails to return a deterministic float between 0.0 and 1.0. 

## Setup and Usage
1.  Build the container:
    `docker build -t openenv-email-triage .`
2.  Run the container:
    `docker run -e HF_TOKEN="your_huggingface_token" openenv-email-triage`

## Baseline Performance
Using Meta Llama 3 70B via the Hugging Face inference API proxy:
*   Task 1: 1.0
*   Task 2: 1.0
*   Task 3: 0.66 - 1.0
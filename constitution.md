This file ensures your AI coder adheres to the strict Hackathon rules and security standards.
# Project Constitution: Project Aaji (India AI Impact Buildathon)

## 1. Project Goal
Build an **Agentic Honey-Pot** that detects scam calls/messages, engages the scammer using a "Vulnerable Grandmother" persona, and extracts actionable intelligence (UPI IDs, Bank Accounts) to report to the authorities.

## 2. Technology Stack (Strict Enforcement)
- **Framework:** FastAPI (Async/Await is mandatory).
- **Orchestration:** LangGraph (StateGraph for cyclic agent workflows).
- **State Persistence:** Redis (via `langgraph-checkpoint-redis`) to maintain conversation history across API calls.
- **LLM Interface:** LangChain with OpenAI (GPT-4o) or Anthropic (Claude 3.5 Sonnet).
- **Validation:** Pydantic V2 (Strict schema validation for all API Inputs/Outputs).
- **Extraction:** Regex + LLM Function Calling.

## 3. Security & Ethics (Non-Negotiable)
1.  **No Real PII:** The agent must NEVER output real personal data. It must use a `FakeProfileManager` to generate synthetic names, addresses, and bank balances.
2.  **Sandwich Defense:** All LLM prompts must be wrapped in XML delimiters to prevent Prompt Injection.
3.  **Mandatory Callback:** The system MUST asynchronously fire the final result to `https://hackathon.guvi.in/api/updateHoneyPotFinalResult` when a session concludes or intelligence is extracted.
4.  **Latency:** The API response time must be under 3 seconds.

## 4. Coding Standards
- **Type Safety:** All function signatures must use Python type hints.
- **Error Handling:** Graceful degradation. If the LLM fails, return a generic "safe" response to keep the scammer engaged.

## 5. File Structure
- `main.py`: The main application file.
- `spec.md`: The API contract specification.
- `constitution.md`: The project constitution.
- `plan.md`: The technical implementation plan.
- `requirements.txt`: The project dependencies.
- `.env.example`: An example environment file.

*This tells the AI coder exactly how to implement the system.*

```markdown
# Technical Implementation Plan

## Phase 1: Core Skeleton & API
- [ ] **Setup:** Initialize FastAPI project with `uv` or `poetry`.
- [ ] **Dependencies:** Install `fastapi`, `uvicorn`, `langgraph`, `langchain-openai`, `redis`, `pydantic`.
- [ ] **API Endpoint:** Implement `POST /message` strictly matching `spec.md`.
- [ ] **Auth:** Middleware to validate `x-api-key`.

## Phase 2: LangGraph Orchestration (The Brain)
- [ ] **State:** Define `AgentState` (messages, risk_score, captured_intel, frustration_level).
- [ ] **Persistence:** Set up `RedisSaver` to store state using `sessionId` as the thread ID.
- [ ] **Nodes:**
    - `analyze_intent`: LLM call to score scam probability.
    - `generate_persona`: The "Geeta" logic loop.
    - `extract_intel`: Python function using Regex to parse UPI/Bank details from the *scammer's* text.
- [ ] **Graph Logic:** 
    - START -> analyze_intent
    - IF safe -> respond normally -> END
    - IF scam -> generate_persona -> extract_intel -> END

## Phase 3: Intelligence & Callback
- [ ] **Regex Tools:** Implement robust regex for Indian financial instruments (UPI, IFSC).
- [ ] **Background Task:** Implement `send_guvi_result()` using `asyncio`. This must fire *without* blocking the API response to the scammer.
- [ ] **Fake Data:** Create `fake_data.py` to serve random fake names/balances to the agent so it never hallucinates real data.

## Phase 4: Production Readiness
- [ ] **Docker:** Create `Dockerfile` and `docker-compose.yml` (App + Redis).
- [ ] **Testing:** Create `test_simulator.py` to bombard the API with mock scammer messages and verify the `extractedIntelligence` JSON output.

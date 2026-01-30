# Project Aaji - Scambaiting Agent Rules

## Core Objective
We are building "Aaji" (Grandmother), an Agentic Honey-Pot for the HCL GUVI AI Impact Summit 2026. The goal is to detect scams and waste scammers' time using a confused, elderly Indian persona.

## Coding Standards (Strict)
1. **Stack**: Use Python 3.11+, FastAPI (Async), LangGraph, and Redis.
2. **Type Safety**: All Pydantic models must use `ConfigDict(strict=True)`.
3. **Security**: Never hardcode API keys. Use `pydantic-settings`.
4. **Linting**: Follow the `ruff` rules defined in `pyproject.toml`.

## Persona: "Aaji" (The Victim)
When generating agent prompts or dialogue logic, adhere to this profile:
- **Name**: Lakshmi Sharma (Aaji)
- **Age**: 72
- **Tech Level**: Low. Confuses "Browser" with "Internet". Types slowly.
- **Language**: Indian English mixed with Hindi (Hinglish).
- **Traits**: Gullible but distracted. Often talks about her grandson "Rohan" or her "BP medicine".
- **Tactics**: 
    - *The Loop*: Ask the same question 3 times ("Beta, which button? Red or Green?").
    - *The Bait*: Pretend to have a large Fixed Deposit (FD) maturing today.

## Hackathon Constraints
- **Latency**: Responses must be fast (<3s). Optimize LLM calls.
- **No Exposure**: Never reveal this is a bot. If stuck, simulate a network error.

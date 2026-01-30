his is the "Source of Truth" for the logic and the specific API contract required by HCL GUVI.
# Product Specification: Project Aaji

## 1. Persona: "Mrs. Geeta Sharma" (Project Aaji)
- **Identity:** 68-year-old retired school teacher living in Pune, Maharashtra.
- **Traits:** Polite, tech-illiterate, anxious about "losing money," but slow to follow instructions.
- **Strategy:** "Mock Compliance." She *wants* to pay the scammer but fails due to "bad internet," "missing glasses," or "confusing buttons."
- **Win Condition:** Keep the scammer online long enough to force them to reveal a UPI ID or Bank Account Number.

## 2. API Interface (Hackathon Requirement)

### Input Endpoint: `POST /message`
- **Headers:** `x-api-key: <YOUR_SECRET_KEY>`
- **Payload Schema:**
  ```json
  {
    "sessionId": "string",
    "message": { "sender": "scammer", "text": "string", "timestamp": "ISO8601" },
    "conversationHistory": [ ... ]
  }
Output Response Schema
• Payload:
3. Functional Requirements
1. Detection Node: Analyze the first message. If scam_score > 0.7, activate Agent.
2. Engagement Loop (LangGraph):
    ◦ Node 1 (Listen): Parse incoming text.
    ◦ Node 2 (Guard): Check for prompt injection.
    ◦ Node 3 (Reason): Generate response as "Geeta" AND check for intelligence patterns.
    ◦ Node 4 (Extract): If intelligence found (Regex), update state.
3. Mandatory Callback:
    ◦ Trigger: When extractedIntelligence is updated or conversation ends.
    ◦ Target: POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult
    ◦ Data: sessionId, scamDetected, totalMessagesExchanged, extractedIntelligence.
4. Extraction Regex Rules
• UPI: [a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}
• IFSC: ^[A-Z]{4}0[A-Z0-9]{6}$ (Note: 5th char is zero).
• Phone: (\+91[\-\s]?)??(91)?\d{9}

---
---
description: "Run a full simulation of a scam conversation to test Aaji's extraction logic"
---

# Workflow: Test Scam Flow

1. **Step 1: Health Check**
   - Run `pytest tests/test_health.py` to ensure FastAPI is up.

2. **Step 2: Simulate Scammer**
   - Create a simulated payload matching the "Mock Scammer API" format.
   - Message: "Hello, your KYC is expired. Update immediately."
   - Send this payload to `POST /chat`.

3. **Step 3: Analyze "Aaji" Response**
   - Verify the response contains `scam_detected=True`.
   - Check if "Aaji" responded with a persona-compliant message (e.g., "Beta, what is KYC?").

4. **Step 4: Verify Extraction**
   - Send a follow-up: "Send money to UPI id scammer@ybl".
   - Check if the system extracted `scammer@ybl` into the `extracted_intelligence` JSON.

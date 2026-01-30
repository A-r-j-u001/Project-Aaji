import asyncio
import json

import httpx

BASE_URL = "http://localhost:8002"

async def run_simulation():
    print(f"Testing against {BASE_URL}")
    
    # 1. Health Check (Simulated by checking connection)
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # We expect 404 on root, but if we get it, server is up.
            resp = await client.get(BASE_URL + "/")
            print("Server is up (Got response).")
        except Exception as e:
            print(f"Server down: {e}")
            return

        # 2. Simulate Scammer (KYC)
        print("\n--- Test 1: Scam Detection (KYC) ---")
        payload_kyc = {
            "sessionId": "test-session-1",
            "message": {
                "sender": "scammer",
                "text": "Hello, your KYC is expired. Update immediately.",
                "timestamp": "2024-01-30T10:00:00Z"
            },
            "conversation_history": [],
            "metadata": {}
        }
        
        headers = {"x-api-key": "YOUR_SECRET_KEY"}
        
        resp = await client.post(f"{BASE_URL}/chat", json=payload_kyc, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print("Response:", json.dumps(data, indent=2))
            print("Response:", json.dumps(data, indent=2))
            # Verify Simplified Response
            assert data["status"] == "success"
            assert "reply" in data
            print(f"Agent Reply: {data['reply']}")
            print("PASSED: Sync response valid.")
        else:
            print(f"FAILED: {resp.status_code} {resp.text}")

        # 3. Simulate Scammer (Extraction)
        print("\n--- Test 2: Extraction (UPI) ---")
        payload_upi = {
            "sessionId": "test-session-1",
            "message": {
                "sender": "scammer",
                "text": "Send 5000rs to my UPI id badguy@okaxis",
                "timestamp": "2024-01-30T10:05:00Z"
            },
            "conversation_history": [], # In real flow we'd append history
            "metadata": {}
        }
        
        resp = await client.post(f"{BASE_URL}/chat", json=payload_upi, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            print("Response:", json.dumps(data, indent=2))
            
            # Verify Simplified Response (Section 8)
            assert data["status"] == "success"
            assert "reply" in data
            print(f"Agent Reply: {data['reply']}")
            
            # Note: Intelligence is now sent via BACKGROUND CALLBACK.
            # In a real integration test, we would mock the callback receiver.
            # Here we just verify the sync response is clean.
            print("PASSED: Sync response valid. Check server logs for [CALLBACK].")
        else:
            print(f"FAILED: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    asyncio.run(run_simulation())

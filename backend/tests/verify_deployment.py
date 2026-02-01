import asyncio
import json
import time

import httpx

# Your PUBLIC URL from localtunnel
# Update this if the tunnel restarts and gives a new URL
PUBLIC_URL = "https://legal-zebras-clean.loca.lt/chat"

API_KEY = "YOUR_SECRET_KEY"

async def verify_deployment():
    print(f"--- Verifying Deployment: {PUBLIC_URL} ---")
    
    payload = {
        "sessionId": "judge-test-001",
        "message": {
            "text": "Hello, I am calling from your bank regarding a KYC update.",
            "sender": "scammer",
            "timestamp": "2026-01-30T10:00:00Z"
        },
        "conversationHistory": []
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
        # This header helps bypass the LocalTunnel warning page just in case
        "Bypass-Tunnel-Reminder": "true" 
    }
    
    start_time = time.time()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            print("Sending POST request...")
            response = await client.post(PUBLIC_URL, json=payload, headers=headers)
            
            latency = time.time() - start_time
            print(f"Latency: {latency:.2f} seconds")
            
            if response.status_code == 200:
                print("\nSUCCESS! Server responded 200 OK.")
                print("Response JSON:")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"\nFAILED. Status Code: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"\nERROR: Could not connect to {PUBLIC_URL}")
            print(f"Detail: {e}")

if __name__ == "__main__":
    asyncio.run(verify_deployment())

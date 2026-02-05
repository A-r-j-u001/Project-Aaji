# Quick Diagnosis Script - Test Endpoint Directly

import requests
import json

# Test payload from GUVI documentation
payload = {
    "sessionId": "quick-test-001",
    "message": {
        "sender": "scammer",
        "text": "URGENT: Your bank account has been compromised. Share your account number immediately.",
        "timestamp": 1770205147568
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

headers = {
    "x-api-key": "hackathon-secret-123",
    "Content-Type": "application/json"
}

print("Testing endpoint...")
print(f"Payload: {json.dumps(payload, indent=2)}\n")

try:
    response = requests.post(
        "https://project-aaji.vercel.app/message",
        json=payload,
        headers=headers,
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print("\nResponse Body:")
    print(json.dumps(response.json(), indent=2))
    
    # Validate response format
    resp_json = response.json()
    if "status" in resp_json and "reply" in resp_json:
        print("\n✅ Response format is CORRECT")
        print(f"   - status: {resp_json['status']}")
        print(f"   - reply: {resp_json['reply']}")
    else:
        print("\n❌ Response format is INCORRECT")
        print(f"   Missing fields. Got: {list(resp_json.keys())}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
except json.JSONDecodeError as e:
    print(f"❌ Invalid JSON response: {e}")
    print(f"Raw response: {response.text}")

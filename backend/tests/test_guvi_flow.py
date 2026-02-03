import requests
import json
import uuid

def test_guvi_flow():
    url = "http://localhost:8000/message"
    
    # Matches the schema expected by the backend
    payload = {
        "sessionId": str(uuid.uuid4()),
        "message": {
            "sender": "scammer",
            "text": "Hello, pay urgently. Sending money to account 1234567890 at http://malicious.com. Urgent verify now.",
            "timestamp": "2024-02-01T10:00:00Z"
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "whatsapp"
        }
    }
    
    headers = {
        "x-api-key": "hackathon-secret-123",
        "Content-Type": "application/json"
    }

    print(f"Sending POST request to {url}...")
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
        
        if response.status_code == 200:
            print("\n✅ Test Passed: Endpoint is reachable and processing requests.")
        else:
            print("\n❌ Test Failed: valid status code.")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Refused: Is the backend server running on port 8000?")

if __name__ == "__main__":
    test_guvi_flow()

import requests
import json
import uuid

def test_public_url():
    # URL from the Serveo output
    url = "https://4a3799ccac2590d8-103-157-5-241.serveousercontent.com/message"
    
    payload = {
        "sessionId": str(uuid.uuid4()),
        "message": {
            "sender": "scammer",
            "text": "Hello, KYC check.",
            "timestamp": "2024-02-01T10:00:00Z"
        },
        "conversationHistory": [],
        "metadata": {"channel": "whatsapp"}
    }
    
    headers = {
        "x-api-key": "hackathon-secret-123",
        "Content-Type": "application/json"
    }

    print(f"Testing Public URL: {url}")
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_public_url()

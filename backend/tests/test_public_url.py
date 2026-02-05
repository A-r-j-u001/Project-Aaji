import httpx
import uuid

def test_public_url():
    # URL from the Serveo output
    url = "https://d84838cff887d4c8-103-167-95-177.serveousercontent.com/message"
    
    payload = {
        "sessionId": str(uuid.uuid4()),
        "message": {
            "sender": "scammer",
            "text": "Your account needs KYC update urgently. Send OTP to verify.",
            "timestamp": "2024-02-03T10:00:00Z"
        },
        "conversationHistory": [],
        "metadata": {"channel": "whatsapp"}
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "hackathon-secret-123"
    }
    
    print(f"Testing Public URL: {url}")
    response = httpx.post(url, json=payload, headers=headers, timeout=30.0)
    print(f"Status Code: {response.status_code}")
    print(response.text)

if __name__ == "__main__":
    test_public_url()

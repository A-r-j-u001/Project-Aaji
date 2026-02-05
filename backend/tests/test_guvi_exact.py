import httpx

def test_guvi_exact_format():
    """Test with EXACT format GUVI sends (integer timestamp)"""
    url = "https://9d166fea03db4d1b-103-167-95-177.serveousercontent.com/message"
    
    # EXACT payload format from GUVI documentation
    payload = {
        "sessionId": "wertyu-dfghj-ertyui",
        "message": {
            "sender": "scammer",
            "text": "Your bank account will be blocked today. Verify immediately.",
            "timestamp": 1770005528731  # Integer epoch milliseconds
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "English",
            "locale": "IN"
        }
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "hackathon-secret-123"
    }
    
    print(f"Testing GUVI Format at: {url}")
    print(f"Payload: {payload}")
    
    try:
        response = httpx.post(url, json=payload, headers=headers, timeout=30.0)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Verify response format
        data = response.json()
        if "status" in data and "reply" in data:
            print("✅ Response format is CORRECT!")
        else:
            print("❌ Response format is WRONG")
            
    except Exception as e:
        print(f"❌ Request Failed: {e}")

if __name__ == "__main__":
    test_guvi_exact_format()

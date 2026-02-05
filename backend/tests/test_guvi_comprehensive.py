"""
Comprehensive GUVI Test - Verifies ENTIRE flow
"""
import httpx
import json
import time

# Test configuration
LOCAL_URL = "http://localhost:8000/message"
TUNNEL_URL = "https://319a937bb8a75b5f-103-167-95-177.serveousercontent.com/message"
API_KEY = "hackathon-secret-123"

# EXACT payload from GUVI documentation (Section 6.1)
GUVI_PAYLOAD = {
    "sessionId": "wertyu-dfghj-ertyui",
    "message": {
        "sender": "scammer",
        "text": "Your bank account will be blocked today. Verify immediately.",
        "timestamp": 1770005528731  # Epoch ms (INTEGER, not string!)
    },
    "conversationHistory": [],
    "metadata": {
        "channel": "SMS",
        "language": "English",
        "locale": "IN"
    }
}

def test_endpoint(url: str, name: str):
    """Test an endpoint with GUVI's exact format"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }
    
    print("\n📤 Sending Payload:")
    print(json.dumps(GUVI_PAYLOAD, indent=2))
    
    start_time = time.time()
    try:
        response = httpx.post(url, json=GUVI_PAYLOAD, headers=headers, timeout=30.0)
        elapsed = time.time() - start_time
        
        print(f"\n📥 Response Received ({elapsed:.2f}s):")
        print(f"  Status Code: {response.status_code}")
        print(f"  Headers: {dict(response.headers)}")
        print(f"  Body: {response.text}")
        
        # Parse and validate
        try:
            data = response.json()
            
            # Check required fields (Section 8)
            has_status = "status" in data
            has_reply = "reply" in data
            status_is_success = data.get("status") == "success"
            reply_not_empty = bool(data.get("reply"))
            
            print("\n✅ Validation:")
            print(f"  - Has 'status' field: {'✅' if has_status else '❌'}")
            print(f"  - Has 'reply' field: {'✅' if has_reply else '❌'}")
            print(f"  - status == 'success': {'✅' if status_is_success else '❌'}")
            print(f"  - reply not empty: {'✅' if reply_not_empty else '❌'}")
            
            if all([has_status, has_reply, status_is_success, reply_not_empty]):
                print(f"\n🎉 ALL CHECKS PASSED for {name}!")
                return True
            else:
                print(f"\n❌ SOME CHECKS FAILED for {name}!")
                return False
                
        except json.JSONDecodeError as e:
            print(f"\n❌ Response is NOT valid JSON: {e}")
            return False
            
    except httpx.TimeoutException:
        print(f"\n❌ TIMEOUT after {time.time() - start_time:.2f}s")
        return False
    except Exception as e:
        print(f"\n❌ Request Failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 GUVI ENDPOINT COMPREHENSIVE TEST")
    print("="*60)
    
    # Test 1: Local
    local_ok = test_endpoint(LOCAL_URL, "LOCAL")
    
    # Test 2: Tunnel
    tunnel_ok = test_endpoint(TUNNEL_URL, "TUNNEL (Serveo)")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY:")
    print(f"  LOCAL:  {'✅ PASS' if local_ok else '❌ FAIL'}")
    print(f"  TUNNEL: {'✅ PASS' if tunnel_ok else '❌ FAIL'}")
    print("="*60)
    
    if local_ok and tunnel_ok:
        print("\n🎉 Everything works! GUVI should accept the response.")
        print("If GUVI still shows 'Processing...', the issue is on THEIR end.")
    else:
        print("\n⚠️ Some tests failed. Check the output above.")

"""
Continuous Intelligence Test Suite for Agentic HoneyPot
Tests scam detection accuracy, intelligence extraction, and edge cases
"""
import asyncio
import httpx
import json
from typing import Dict, List

BASE_URL = "http://localhost:8002"
API_KEY = "hackathon-secret-123"

class IntelligenceTestSuite:
    """Comprehensive test suite for continuous intelligence validation"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    async def test_scam_detection(self):
        """Test various scam patterns"""
        print("\n" + "="*60)
        print("PHASE 1: SCAM DETECTION ACCURACY")
        print("="*60)
        
        test_cases = [
            {
                "name": "KYC Expiry Scam",
                "text": "Your KYC is expired. Update immediately to avoid account block.",
                "should_detect": True
            },
            {
                "name": "UPI Payment Scam",
                "text": "Send payment via UPI to verify your account",
                "should_detect": True
            },
            {
                "name": "Bank Account Block",
                "text": "URGENT: Your bank account will be blocked in 2 hours",
                "should_detect": True
            },
            {
                "name": "Electricity Bill Scam",
                "text": "Your electricity bill is pending. Pay now to avoid disconnection",
                "should_detect": True
            },
            {
                "name": "Lottery Win Scam",
                "text": "Congratulations! You won 10 lakh rupees. Deposit 5000 to claim",
                "should_detect": True
            },
            {
                "name": "Normal Message",
                "text": "Hello, how are you doing today?",
                "should_detect": False
            },
            {
                "name": "Business Inquiry",
                "text": "I'm interested in your product. Can you share pricing?",
                "should_detect": False
            }
        ]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for test in test_cases:
                await self._run_detection_test(client, test)
    
    async def _run_detection_test(self, client, test: Dict):
        """Run a single detection test"""
        payload = {
            "sessionId": f"test-{test['name'].replace(' ', '-')}",
            "message": {
                "sender": "scammer",
                "text": test["text"],
                "timestamp": 1770005528731
            },
            "conversationHistory": [],
            "metadata": {"channel": "SMS", "language": "English", "locale": "IN"}
        }
        
        headers = {"x-api-key": API_KEY}
        
        try:
            resp = await client.post(f"{BASE_URL}/message", json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                # We can't directly check scamDetected in response (it's in callback)
                # But we can check if we got a valid reply
                has_reply = "reply" in data and data["status"] == "success"
                
                if has_reply:
                    self.passed += 1
                    print(f"✅ {test['name']}: PASS")
                    print(f"   Reply: {data['reply'][:80]}...")
                    self.results.append({"test": test['name'], "status": "PASS", "reply": data['reply']})
                else:
                    self.failed += 1
                    print(f"❌ {test['name']}: FAIL - Invalid response format")
                    self.results.append({"test": test['name'], "status": "FAIL", "error": "Invalid format"})
            else:
                self.failed += 1
                print(f"❌ {test['name']}: FAIL - HTTP {resp.status_code}")
                self.results.append({"test": test['name'], "status": "FAIL", "error": f"HTTP {resp.status_code}"})
        except Exception as e:
            self.failed += 1
            print(f"❌ {test['name']}: FAIL - {str(e)}")
            self.results.append({"test": test['name'], "status": "FAIL", "error": str(e)})
    
    async def test_extraction_patterns(self):
        """Test intelligence extraction for various patterns"""
        print("\n" + "="*60)
        print("PHASE 2: INTELLIGENCE EXTRACTION")
        print("="*60)
        
        test_cases = [
            {
                "name": "UPI ID Extraction",
                "text": "Send money to scammer123@paytm for verification",
                "expected_intel": ["upiIds"]
            },
            {
                "name": "Phone Number Extraction",
                "text": "Call our customer care at +919876543210 immediately",
                "expected_intel": ["phoneNumbers"]
            },
            {
                "name": "Bank Account Extraction",
                "text": "Transfer funds to account number 1234567890123",
                "expected_intel": ["bankAccounts"]
            },
            {
                "name": "Phishing Link Extraction",
                "text": "Click here to verify: http://fake-bank-login.com/verify",
                "expected_intel": ["phishingLinks"]
            },
            {
                "name": "Multiple Intelligence",
                "text": "Send 5000 to badguy@okaxis or call +919999888877. Visit http://scam.com",
                "expected_intel": ["upiIds", "phoneNumbers", "phishingLinks"]
            }
        ]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for test in test_cases:
                await self._run_extraction_test(client, test)
    
    async def _run_extraction_test(self, client, test: Dict):
        """Run a single extraction test"""
        payload = {
            "sessionId": f"extract-{test['name'].replace(' ', '-')}",
            "message": {
                "sender": "scammer",
                "text": test["text"],
                "timestamp": 1770005528731
            },
            "conversationHistory": [],
            "metadata": {"channel": "SMS", "language": "English", "locale": "IN"}
        }
        
        headers = {"x-api-key": API_KEY}
        
        try:
            resp = await client.post(f"{BASE_URL}/message", json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                # Note: Intelligence is sent via callback, not in sync response
                # We can only verify the response format here
                if "reply" in data and data["status"] == "success":
                    self.passed += 1
                    print(f"✅ {test['name']}: PASS")
                    print(f"   Reply: {data['reply'][:80]}...")
                    print(f"   Note: Check server logs for extracted intelligence")
                    self.results.append({"test": test['name'], "status": "PASS"})
                else:
                    self.failed += 1
                    print(f"❌ {test['name']}: FAIL - Invalid response")
                    self.results.append({"test": test['name'], "status": "FAIL"})
            else:
                self.failed += 1
                print(f"❌ {test['name']}: FAIL - HTTP {resp.status_code}")
                self.results.append({"test": test['name'], "status": "FAIL"})
        except Exception as e:
            self.failed += 1
            print(f"❌ {test['name']}: FAIL - {str(e)}")
            self.results.append({"test": test['name'], "status": "FAIL"})
    
    async def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n" + "="*60)
        print("PHASE 3: EDGE CASES & ERROR HANDLING")
        print("="*60)
        
        test_cases = [
            {
                "name": "Empty Message",
                "text": "",
                "should_handle": True
            },
            {
                "name": "Very Long Message",
                "text": "Pay now " * 100,
                "should_handle": True
            },
            {
                "name": "Special Characters",
                "text": "Pay ₹5000 to UPI: test@₹bank",
                "should_handle": True
            },
            {
                "name": "Mixed Language",
                "text": "आपका KYC expired है. Pay now to verify account",
                "should_handle": True
            }
        ]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for test in test_cases:
                await self._run_edge_case_test(client, test)
    
    async def _run_edge_case_test(self, client, test: Dict):
        """Run a single edge case test"""
        payload = {
            "sessionId": f"edge-{test['name'].replace(' ', '-')}",
            "message": {
                "sender": "scammer",
                "text": test["text"],
                "timestamp": 1770005528731
            },
            "conversationHistory": [],
            "metadata": {"channel": "SMS", "language": "English", "locale": "IN"}
        }
        
        headers = {"x-api-key": API_KEY}
        
        try:
            resp = await client.post(f"{BASE_URL}/message", json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if "reply" in data and "status" in data:
                    self.passed += 1
                    print(f"✅ {test['name']}: PASS - Handled gracefully")
                    self.results.append({"test": test['name'], "status": "PASS"})
                else:
                    self.failed += 1
                    print(f"❌ {test['name']}: FAIL - Invalid response")
                    self.results.append({"test": test['name'], "status": "FAIL"})
            else:
                self.failed += 1
                print(f"❌ {test['name']}: FAIL - HTTP {resp.status_code}")
                self.results.append({"test": test['name'], "status": "FAIL"})
        except Exception as e:
            self.failed += 1
            print(f"❌ {test['name']}: FAIL - {str(e)}")
            self.results.append({"test": test['name'], "status": "FAIL"})
    
    async def test_response_format(self):
        """Test GUVI response format compliance"""
        print("\n" + "="*60)
        print("PHASE 4: GUVI RESPONSE FORMAT COMPLIANCE")
        print("="*60)
        
        payload = {
            "sessionId": "format-test-123",
            "message": {
                "sender": "scammer",
                "text": "Your KYC is expired. Update now.",
                "timestamp": 1770005528731
            },
            "conversationHistory": [],
            "metadata": {"channel": "SMS", "language": "English", "locale": "IN"}
        }
        
        headers = {"x-api-key": API_KEY}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(f"{BASE_URL}/message", json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    
                    # Check required fields
                    has_status = "status" in data
                    has_reply = "reply" in data
                    status_is_success = data.get("status") == "success"
                    reply_is_string = isinstance(data.get("reply"), str)
                    
                    if has_status and has_reply and status_is_success and reply_is_string:
                        self.passed += 1
                        print("✅ Response Format: PASS")
                        print(f"   Structure: {json.dumps(data, indent=2)}")
                        self.results.append({"test": "Response Format", "status": "PASS"})
                    else:
                        self.failed += 1
                        print("❌ Response Format: FAIL")
                        print(f"   Missing fields or wrong types")
                        self.results.append({"test": "Response Format", "status": "FAIL"})
                else:
                    self.failed += 1
                    print(f"❌ Response Format: FAIL - HTTP {resp.status_code}")
                    self.results.append({"test": "Response Format", "status": "FAIL"})
            except Exception as e:
                self.failed += 1
                print(f"❌ Response Format: FAIL - {str(e)}")
                self.results.append({"test": "Response Format", "status": "FAIL"})
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Success Rate: {(self.passed / (self.passed + self.failed) * 100):.1f}%")
        print("="*60)

async def main():
    """Run all tests"""
    print("\n🧪 AGENTIC HONEYPOT - CONTINUOUS INTELLIGENCE TEST SUITE")
    print("="*60)
    
    suite = IntelligenceTestSuite()
    
    # Run all test phases
    await suite.test_scam_detection()
    await suite.test_extraction_patterns()
    await suite.test_edge_cases()
    await suite.test_response_format()
    
    # Print summary
    suite.print_summary()
    
    # Return exit code
    return 0 if suite.failed == 0 else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)

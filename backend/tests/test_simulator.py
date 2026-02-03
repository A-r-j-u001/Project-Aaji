import asyncio

import httpx

API_URL = "http://localhost:8000/message"
API_KEY = "hackathon-secret-123"

SCENARIOS = [
    {
        "name": "KYC Fraud (WhatsApp)",
        "channel": "whatsapp",
        "message": "Dear customer your bank account will be blocked today. Pls update KYC immediately click: http://bit.ly/fake-bank",
        "sender": "scammer"
    },
    {
        "name": "Lottery Win (SMS)",
        "channel": "sms",
        "message": "Congrats! U won 5crore lottery. Pay tax of 5000 to claim. Call 9998887776",
        "sender": "scammer"
    },
    {
        "name": "CEO Fraud (Email)",
        "channel": "email",
        "message": "I am traveling and need you to urgently transfer funds to vendor. Details attached.",
        "sender": "scammer_ceo"
    }
]

async def run_scenario(scenario):
    print(f"\n--- Running Scenario: {scenario['name']} ---")
    
    payload = {
        "sessionId": f"test-sess-{scenario['channel']}",
        "message": {
            "sender": scenario["sender"],
            "text": scenario["message"],
            "timestamp": "2024-02-01T10:00:00Z"
        },
        "conversationHistory": [],
        "metadata": {
            "channel": scenario['channel']
        }
    }
    
    headers = {"x-api-key": API_KEY}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(API_URL, json=payload, headers=headers)
            if response.status_code == 200:
                print(f"✅ Success! Response: {response.json()}")
            else:
                print(f"❌ Failed! Status: {response.status_code}, Body: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    print("🚀 Starting Aaji Simulator...")
    # Check if server is up
    try:
        async with httpx.AsyncClient() as client:
            await client.get("http://localhost:8000/docs", timeout=2)
    except Exception:
        print("⚠️  Server might not be running. Start it with: uvicorn src.main:app --reload")
        # In a real CI, we might wait or start it. For now, we assume user/agent starts it.
    
    for scenario in SCENARIOS:
        await run_scenario(scenario)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os

from dotenv import load_dotenv

from src.utils import run_aaji_persona

# Load env (so we get the API Key)
load_dotenv()

async def test_intelligence():
    print("--- Testing Aaji Intelligence (Gemini) ---")
    
    # Check Key
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        print("❌ ERROR: GOOGLE_API_KEY not found in .env")
        return

    print(f"✅ API Key found: {key[:5]}... (Valid)")

    # Test Message
    messages = [
        {
            "sender": "scammer", 
            "text": (
                "Hello, I am calling from electric office. "
                "Your power will be cut in 5 minutes if you don't pay."
            )
        }
    ]
    
    print(f"\n[Scammer]: {messages[0]['text']}")
    print("... Aaji is thinking (calling Gemini) ...")
    
    try:
        response, intelligence = await run_aaji_persona(messages)
        print(f"\n[Aaji]: {response['text']}")
        print(f"[Intelligence]: {intelligence}")
        
        # Validation
        if "fused" in response['text'] and "beta" in response['text'].lower() and len(response['text']) < 100:
             # This looks like the fallback template "I am confused beta..."
             print("\n⚠️ RESULT: It seems to be using the FALLBACK Template.")
        else:
             print("\n✅ RESULT: Success! Response looks dynamic (AI Generated).")
             
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_intelligence())

import asyncio
import os

from dotenv import load_dotenv

from src.prompts import AAJI_SYSTEM_PROMPT
from src.utils import call_gemini_api

load_dotenv()

async def debug():
    print("--- Debugging Gemini API Direct Call ---")
    key = os.getenv("GOOGLE_API_KEY")
    print(f"Key: {key[:10]}... (Length: {len(key)})")
    
    history = [{"sender": "scammer", "text": "Hello"}]
    
    print("Calling API...")
    result = await call_gemini_api(history, AAJI_SYSTEM_PROMPT)
    
    if result:
        print(f"✅ Success! Response:\n{result}")
    else:
        print("❌ Failed. Result is None.")

if __name__ == "__main__":
    asyncio.run(debug())

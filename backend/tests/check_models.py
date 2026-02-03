import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

async def check_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    base_url = "https://generativelanguage.googleapis.com/v1beta/"
    
    candidates = [
        "models/gemini-1.5-flash",
        "models/gemini-1.5-pro",
        "models/gemini-pro",
        "models/gemini-2.0-flash-exp",
        "models/gemini-1.0-pro"
    ]
    
    print(f"Checking {len(candidates)} models...")
    
    async with httpx.AsyncClient() as client:
        for model in candidates:
            url = f"{base_url}{model}:generateContent?key={api_key}"
            try:
                payload = {"contents": [{"parts": [{"text": "Hi"}]}]}
                resp = await client.post(url, json=payload, timeout=5)
                if resp.status_code == 200:
                    print(f"✅ WORKS: {model}")
                    return
                else:
                    print(f"❌ {model}: {resp.status_code} ({resp.text[:50]}...)")
            except Exception as e:
                print(f"⚠️ Error {model}: {e}")

if __name__ == "__main__":
    asyncio.run(check_models())

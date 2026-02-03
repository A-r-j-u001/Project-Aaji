import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

async def check():
    api_key = os.getenv("GOOGLE_API_KEY")
    # Using the name exactly as listed (deduced from previous output)
    model = "models/gemini-3-flash-preview" 
    url = f"https://generativelanguage.googleapis.com/v1beta/{model}:generateContent?key={api_key}"
    
    print(f"Testing: {model}")
    
    async with httpx.AsyncClient() as client:
        payload = {"contents": [{"parts": [{"text": "Hi"}]}]}
        resp = await client.post(url, json=payload, timeout=5)
        if resp.status_code == 200:
            print(f"✅ WORKS: {model}")
            print(resp.json())
        else:
            print(f"❌ Failed: {resp.status_code} ({resp.text})")

if __name__ == "__main__":
    asyncio.run(check())

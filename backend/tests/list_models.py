import asyncio
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

async def list_models():
    api_key = os.getenv("GOOGLE_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    print(f"Querying: {url.replace(api_key, 'HIDDEN')}")
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
             models = resp.json().get("models", [])
             for m in models:
                 if "generateContent" in m["supportedGenerationMethods"]:
                     print(f"- {m['name']}")
        else:
            print(f"Error: {resp.text}")

if __name__ == "__main__":
    asyncio.run(list_models())

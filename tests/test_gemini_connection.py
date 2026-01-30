import asyncio
import os

import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import HarmBlockThreshold, HarmCategory

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

safety_settings = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

async def test_gemini():
    print("Listing available models...")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Found model: {m.name}")
    
    print("\nTesting Gemini Connection with 'gemini-1.5-flash'...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await model.generate_content_async("Hello", safety_settings=safety_settings)
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Failed with gemini-1.5-flash: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())

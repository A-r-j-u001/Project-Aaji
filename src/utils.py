import re
from typing import Dict, Tuple

# Gemini Disabled due to recurring library/env crashes
# import google.generativeai as genai ...

async def check_scam_intent(message: dict) -> bool:
    """
    Uses Keywords to analyze if a message is a scam.
    """
    text = message.get("text", "")
    scam_keywords = ["kyc", "expired", "pay", "upi", "bank", "verify", "update", "deposit", "money", "win", "electricity", "bill"]
    return any(k in text.lower() for k in scam_keywords)

import os
import httpx
import json

# Gemini Configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

async def call_gemini_api(history: list, system_prompt: str) -> str:
    """
    Calls Gemini API via Raw HTTP to avoid SDK crashes.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("DEBUG: No Google API Key found. Fallback to rules.")
        return None

    try:
        # Construct Payload
        contents = [{"role": "user", "parts": [{"text": system_prompt}]}]
        for msg in history:
            role = "model" if msg.get("sender") == "aaji" else "user"
            contents.append({"role": role, "parts": [{"text": msg.get("text", "")}]})
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 150,
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{GEMINI_API_URL}?key={api_key}",
                json=payload,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
            
    except Exception as e:
        print(f"ERROR: Gemini API Failed: {e}")
        return None

async def run_aaji_persona(messages: list) -> Tuple[Dict, Dict]:
    """
    Simulates 'Aaji' engaging the scammer.
    Strategy: Try AI first -> Fallback to Rules.
    """
    print("DEBUG: Entering run_aaji_persona (Hybrid Mode)")
    # 1. Extract Intelligence
    last_user_text = messages[-1].get("text", "")
    extracted = await extract_data(last_user_text)
    
    # 2. Response Logic (Hybrid)
    reply_text = None
    
    # Try AI
    reply_text = await call_gemini_api(messages, AAJI_SYSTEM_PROMPT)
    
    # Fallback to Rule-Based if AI fails
    if not reply_text:
        print("DEBUG: Using Rule-Based Fallback")
        last_msg_lower = last_user_text.lower()
        if extracted.get("upi_id"):
            reply_text = f"Beta, I am trying to send money to {extracted['upi_id']} but my phone says 'Server Error'. Should I go to the ATM?"
        elif extracted.get("phone"):
            reply_text = f"Okay, I will call you on {extracted['phone']}. Please pick up, my hearing aid is buzzing."
        elif "kyc" in last_msg_lower:
            reply_text = "Beta, what is KYC? Is it the same as my pension card? I am very old, please help."
        elif "otp" in last_msg_lower:
            reply_text = "OTP? Is that the number on the back of the card? It is 4... 2... wait I need my glasses."
        elif "card" in last_msg_lower:
             reply_text = "My card is sbi... wait, grandson said never share card details. But you are bank official na?"
        elif "electricity" in last_msg_lower or "bill" in last_msg_lower:
            reply_text = "Light bill? But I paid the man who comes to the door yesterday. Are you from the government?"
        else:
            reply_text = "I am pressing the buttons but nothing is happening. My grandson Rohan usually does this. Can you wait 5 minutes?"
    
    return {
        "text": reply_text,
        "sender": "aaji"
    }, extracted

async def extract_data(text: str) -> Dict:
    """
    Extracts UPI IDs, Phone numbers, etc. using Regex from spec.md.
    """
    extracted = {}
    
    # Regex from spec.md (Improved)
    upi_pattern = r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}'
    phone_pattern = r'(\+91[\-\s]?)?(91)?\d{10}' 
    link_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    upi_matches = re.findall(upi_pattern, text)
    if upi_matches:
        extracted["upiIds"] = upi_matches
        extracted["upi_id"] = upi_matches[0] 

    phone_matches = re.findall(phone_pattern, text)
    if phone_matches:
        extracted["phoneNumbers"] = [m[0] if isinstance(m, tuple) else m for m in phone_matches]
        extracted["phone"] = extracted["phoneNumbers"][0]

    link_matches = re.findall(link_pattern, text)
    if link_matches:
        extracted["phishingLinks"] = link_matches
        
    return extracted

async def send_guvi_callback(payload: dict):
    """
    Simulates sending the mandatory callback to GUVI.
    In real usage, use httpx.post("https://hackathon.guvi.in/api/updateHoneyPotFinalResult", ...)
    """
    import asyncio
    print(f"\n[CALLBACK] Sending intelligence to GUVI: {payload}")
    await asyncio.sleep(0.1)

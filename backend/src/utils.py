import re
from typing import Dict, Tuple

# Gemini Disabled due to recurring library/env crashes
# import google.generativeai as genai ...

SCAM_KEYWORDS = [
    "kyc", "expired", "pay", "upi", "bank", "verify", 
    "update", "deposit", "money", "win", "electricity", "bill",
    "account blocked", "urgent", "verify now" # Added from GUVI example
]

async def check_scam_intent(message: dict) -> bool:
    """
    Uses Keywords to analyze if a message is a scam.
    """
    text = message.get("text", "")
    return any(k in text.lower() for k in SCAM_KEYWORDS)

import os

import httpx

from src.prompts import AGENT_SYSTEM_PROMPT, INTELLIGENCE_PROMPT
import json

# Gemini Configuration
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"

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

async def extract_with_ai(text: str) -> Dict:
    """
    Uses Gemini to extract structured intelligence from text.
    Robust JSON parsing with multiple fallback strategies.
    """
    prompt = INTELLIGENCE_PROMPT.format(text=text)
    response_text = await call_gemini_api([], prompt)
    
    if not response_text:
        return {}
        
    try:
        # Strategy 1: Clean markdown code blocks
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        
        # Strategy 2: Extract JSON from text (handle extra text before/after)
        # Find first { and last }
        start = clean_json.find('{')
        end = clean_json.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            clean_json = clean_json[start:end+1]
        
        # Strategy 3: Remove common formatting issues
        clean_json = clean_json.replace("'", '"')  # Replace single quotes with double quotes
        clean_json = clean_json.strip()
        
        data = json.loads(clean_json)
        return data
    except json.JSONDecodeError as e:
        print(f"WARN: AI Extraction JSON Parse Failed: {e}")
        print(f"Response was: {response_text[:200]}...")  # Log first 200 chars
        # Fallback: Return empty dict, regex will handle extraction
        return {}
    except Exception as e:
        print(f"WARN: AI Extraction Failed: {e}")
        return {}

async def run_agent_persona(messages: list, channel: str = "whatsapp") -> Tuple[Dict, Dict]:
    """
    Simulates the Agent engaging the scammer.
    Strategy: Try AI first -> Fallback to Rules.
    """
    print(f"DEBUG: Entering run_agent_persona (Hybrid Mode) - Channel: {channel}")
    # 1. Extract Intelligence
    last_user_text = messages[-1].get("text", "")
    extracted = await extract_data(last_user_text)
    
    # 2. Response Logic (Hybrid)
    reply_text = None
    
    # Try AI
    formatted_system_prompt = AGENT_SYSTEM_PROMPT.format(channel=channel)
    reply_text = await call_gemini_api(messages, formatted_system_prompt)
    
    # Fallback to Rule-Based if AI fails
    # Neutralized Fallbacks (No Grandma/Hearing Aid)
    if not reply_text:
        print("DEBUG: Using Rule-Based Fallback")
        last_msg_lower = last_user_text.lower()
        if extracted.get("upi_id"):
            reply_text = (
                f"I am trying to send money to {extracted['upi_id']} "
                "but it says 'Payment Failed'. What should I do?"
            )
        elif extracted.get("phone"):
            reply_text = (
                f"Okay, I will call {extracted['phone']}. "
                "Can you please stay on the line?"
            )
        elif "kyc" in last_msg_lower:
            reply_text = (
                "What is this KYC? I updated it last year. "
                "Why is it asking again?"
            )
        elif "otp" in last_msg_lower:
            reply_text = (
                "I am not receiving any code. "
                "Can you send it again?"
            )
        elif "card" in last_msg_lower:
             reply_text = (
                "I have my card but I am scared to share details. "
                "Is this really the bank?"
            )
        elif "electricity" in last_msg_lower or "bill" in last_msg_lower:
            reply_text = (
                "I already paid the bill online. "
                "Why are you saying it is pending?"
            )
        else:
            reply_text = (
                "I don't understand what you mean. "
                "Please explain properly."
            )
    
    return {
        "text": reply_text,
        "sender": "agent"
    }, extracted

# Pre-compiled Regex Patterns (Optimization)
UPI_PATTERN = re.compile(r'[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}')
PHONE_PATTERN = re.compile(r'(\+91[\-\s]?)?(91)?\d{10}')
LINK_PATTERN = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
)
BANK_ACCOUNT_PATTERN = re.compile(r'\b\d{9,18}\b') # Generic 9-18 digit account number
IFSC_PATTERN = re.compile(r'^[A-Z]{4}0[A-Z0-9]{6}$')

async def extract_data(text: str) -> Dict:
    """
    Extracts UPI IDs, Phone numbers, etc. using Hybrid approach (Regex + AI).
    """
    extracted = {}
    
    # 1. AI Extraction (Intelligent Understanding)
    ai_data = await extract_with_ai(text)
    if ai_data:
        extracted["suspiciousKeywords"] = ai_data.get("suspiciousKeywords", [])
        extracted["scamType"] = ai_data.get("scamType")
        extracted["urgencyLevel"] = ai_data.get("urgencyLevel")
    
    # 2. Regex Extraction (Precision for Entities)
    
    upi_matches = UPI_PATTERN.findall(text)
    if upi_matches:
        extracted["upiIds"] = upi_matches
        extracted["upi_id"] = upi_matches[0] 

    phone_matches = PHONE_PATTERN.findall(text)
    if phone_matches:
        # Normalize phone numbers
        clean_phones = [m[0] if isinstance(m, tuple) else m for m in phone_matches]
        extracted["phoneNumbers"] = clean_phones
        extracted["phone"] = clean_phones[0]

    link_matches = LINK_PATTERN.findall(text)
    if link_matches:
        extracted["phishingLinks"] = link_matches

    # Bank Accounts & IFSC
    account_matches = BANK_ACCOUNT_PATTERN.findall(text)
    if account_matches:
        extracted["bankAccounts"] = account_matches
    
    ifsc_matches = IFSC_PATTERN.findall(text)
    if ifsc_matches:
        # Append IFSC to bankAccounts if found, or handle separately if schema changes
        # For now, strict adherence to schema 'bankAccounts'
        current_accounts = extracted.get("bankAccounts", [])
        extracted["bankAccounts"] = current_accounts + ifsc_matches

    # Suspicious Keywords (Merge AI + Rule Based)
    found_keywords = [k for k in SCAM_KEYWORDS if k in text.lower()]
    existing_keywords = extracted.get("suspiciousKeywords", [])
    
    # Merge and deduplicate
    extracted["suspiciousKeywords"] = list(set(found_keywords + existing_keywords))
        
    return extracted

async def send_guvi_callback(payload: dict):
    """
    Simulates sending the mandatory callback to GUVI.
    In real usage, use httpx.post("https://hackathon.guvi.in/api/updateHoneyPotFinalResult", ...)
    """
    import asyncio
    print(f"\n[CALLBACK] Sending intelligence to GUVI: {payload}")
    
    # --- REAL INTEGRATION CODE ---
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://hackathon.guvi.in/api/updateHoneyPotFinalResult", 
                json=payload,
                timeout=5.0
            )
            print(f"[CALLBACK] Response: {resp.status_code}")
    except Exception as e:
        print(f"[CALLBACK] Failed to reach Guvi: {e}")
    # -----------------------------
    await asyncio.sleep(0.1)

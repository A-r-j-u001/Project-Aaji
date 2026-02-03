# Project Aaji - AI Scambaiting Agent 👵🤖

**Submitted for HCL Guvi Hackathon**

## 📢 Project Overview
**Aaji** (Grandmother in Marathi/Hindi) is an autonomous AI Agent designed to waste scammers' time. She adopts the persona of a confused, elderly Indian woman to engage fraudsters on **WhatsApp** and **Instagram**, protecting potential victims by keeping scammers busy and extracting their intelligence (UPI IDs, Phone Numbers).

## 🚀 Live Demo URLs (Active Now)
- **API Base URL**: `https://da279c616d3f6ee3-103-138-9-17.serveousercontent.com`
- **WhatsApp Webhook**: `/twilio/whatsapp`
- **Instagram Webhook**: `/meta/instagram`
- **Standard API Check**: `/message`

## 🛠️ Technology Stack
- **Framework**: Python (FastAPI)
- **AI Brain**: LangGraph (State Machine) + Google Gemini (LLM)
- **Intelligence**: Regex (Pre-compiled with Rust-like optimization logic) + Rule-Based Fallbacks.
- **Hosting**: Serveo Tunneling (Dev Mode)

## 🏃‍♂️ How to Run locally
1. `cd backend`
2. `pip install -r requirements.txt`
3. `python -m uvicorn src.main:app --host 0.0.0.0 --port 8000`

## 🧪 Testing (JSON Payload) - `/message`
```json
{
  "sessionId": "test-123",
  "message": {
    "sender": "scammer",
    "text": "Sir, your KYC is pending, please send OTP.",
    "timestamp": "2024-02-01T10:00:00Z"
  },
  "conversationHistory": [],
  "metadata": {}
}
```
**Expected Response:** a confused reply from Aaji.

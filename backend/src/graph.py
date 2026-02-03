"""
Simple Agent Graph (No LangGraph Dependency)
Uses plain async functions instead of state machine.
"""
from typing import Any, Dict, List

from src.utils import check_scam_intent, run_aaji_persona


async def process_message(messages: List[dict], channel: str = "whatsapp") -> Dict[str, Any]:
    """
    Main entry point - replaces langgraph state machine.
    """
    # Step 1: Detect Intent
    is_scam = await check_scam_intent(messages[-1])
    
    if not is_scam:
        return {
            "status": "success",
            "scamDetected": False,
            "reply": "This doesn't appear to be a scam message.",
            "extractedIntelligence": {},
            "agentNotes": "No scam detected."
        }
    
    # Step 2: Engage Scammer (Aaji Persona)
    response, captured_data = await run_aaji_persona(messages, channel=channel)
    
    return {
        "status": "success",
        "scamDetected": True,
        "extractedIntelligence": captured_data,
        "agentNotes": "Engaging scammer with 'Fixed Deposit' bait.",
        "reply": response["text"]
    }

from typing import Any, Dict, List, TypedDict

from langgraph.graph import END, StateGraph

from src.utils import check_scam_intent, run_aaji_persona


class AgentState(TypedDict):
    messages: List[dict]
    scam_detected: bool
    intelligence: Dict[str, Any]
    final_response: Dict[str, Any]
    channel_context: str

# --- Nodes ---

async def detect_intent(state: AgentState):
    """First line of defense: Is this a scam?"""
    # Use a lightweight model or regex for speed
    is_scam = await check_scam_intent(state["messages"][-1])
    return {"scam_detected": is_scam}

async def engage_scammer(state: AgentState):
    """The 'Aaji' Persona Node"""
    # Uses Gemini to generate a confused grandmother response
    channel = state.get("channel_context", "whatsapp")
    response, captured_data = await run_aaji_persona(state["messages"], channel=channel)
    
    # Update intelligence if we found UPI/Bank details
    new_intel = {**state.get("intelligence", {}), **captured_data}
    
    return {
        "intelligence": new_intel,
        "final_response": {
            "status": "success",
            "scamDetected": True,
            "extractedIntelligence": new_intel,
            "agentNotes": "Engaging scammer with 'Fixed Deposit' bait.",
            "reply": response["text"] # Expose text for the sync response
        }
    }

# --- Graph Construction ---

workflow = StateGraph(AgentState)
workflow.add_node("detect", detect_intent)
workflow.add_node("aaji_bot", engage_scammer)

# Conditional Edge: If scam detected, switch to Aaji. If not, ignore or handoff.
workflow.set_entry_point("detect")
workflow.add_conditional_edges(
    "detect",
    lambda x: "aaji_bot" if x["scam_detected"] else END
)
workflow.add_edge("aaji_bot", END)

aaji_graph = workflow.compile()

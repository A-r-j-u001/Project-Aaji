from dotenv import load_dotenv
load_dotenv() # Load enviroment variables

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException

from src.graph import aaji_graph
from src.schemas import AgentResponse, ScammerInput

app = FastAPI(title="Aaji - Agentic HoneyPot")

@app.post("/chat", response_model=AgentResponse)
async def chat_webhook(
    payload: ScammerInput, 
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(...)
):
    """
    Main entry point for the Mock Scammer API.
    """
    if x_api_key != "YOUR_SECRET_KEY":  # Replace with env var
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # Invoke the LangGraph agent
    # The graph maintains state using the session_id from payload
    # Note: payload.conversationHistory is aliased for input, mapped to snake_case in logic if needed
    initial_state = {
        "messages": payload.conversationHistory + [payload.message.model_dump()],
        "scam_detected": False,
        "intelligence": {},
        "final_response": {}
    }
    
    result = await aaji_graph.ainvoke(initial_state)
    
    final_state = result["final_response"] # Internal full state
    
    # Trigger Callback (Section 12) if scam confirmed
    # We construct the CallbackPayload here or in the graph. 
    # For now, we extract from final_state.
    if final_state.get("scamDetected"):
        from src.schemas import CallbackPayload, ExtractedIntelligence
        from src.utils import send_guvi_callback
        
        # Safe construction of extracted intelligence
        raw_intel = final_state.get("extractedIntelligence", {})
        intel_obj = ExtractedIntelligence(
            bankAccounts=raw_intel.get("bankAccounts", []),
            upiIds=raw_intel.get("upiIds", []),
            phishingLinks=raw_intel.get("phishingLinks", []),
            phoneNumbers=raw_intel.get("phoneNumbers", [])
        )

        callback_data = CallbackPayload(
            sessionId=payload.sessionId,
            scamDetected=True,
            totalMessagesExchanged=len(payload.conversationHistory) + 1,
            extractedIntelligence=intel_obj,
            agentNotes=final_state.get("agentNotes", "Scam detected.")
        )
        
        background_tasks.add_task(send_guvi_callback, callback_data.model_dump())

    # Return Section 8 Format
    return AgentResponse(
        status="success",
        reply=final_state.get("reply", "System Processing...") # We need to map the text reply here
    )

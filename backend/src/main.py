import sys
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
load_dotenv()

# Vercel Path Hack: Ensure the parent directory of 'src' is in sys.path
# File path: /var/task/backend/src/main.py
# We want /var/task/backend in sys.path to do "from src.graph..."
# OR strict relative imports if running as module.
# Let's try adding BOTH the current directory and the parent.

current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent

sys.path.append(str(current_dir)) # Adds /.../backend/src
sys.path.append(str(parent_dir))  # Adds /.../backend

from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Form, Response, Query, Request
from fastapi.responses import JSONResponse

# Lazy imports or try/except to prevent boot crash
try:
    # Try importing as if we are inside 'backend' package
    from src.graph import process_message
    from src.schemas import ScammerInput, Message
except ImportError:
    try:
        # Fallback for when 'src' is local
        from graph import process_message
        from schemas import ScammerInput, Message
    except ImportError as e:
        print(f"CRITICAL IMPORT ERROR: {e}")
        process_message = None
        ScammerInput = Any

app = FastAPI(title="Aaji - Agentic HoneyPot")

# Session Store for Intelligence Aggregation
from typing import Dict

class SessionStore:
    """In-memory store for tracking session intelligence across turns"""
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
    
    def get_session(self, session_id: str) -> dict:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "intelligence": {
                    "bankAccounts": set(),
                    "upiIds": set(),
                    "phishingLinks": set(),
                    "phoneNumbers": set(),
                    "suspiciousKeywords": set()
                },
                "message_count": 0,
                "scam_detected": False
            }
        return self.sessions[session_id]
    
    def update_intelligence(self, session_id: str, new_intel: dict):
        """Merge new intelligence with existing session intelligence"""
        session = self.get_session(session_id)
        for key in ["bankAccounts", "upiIds", "phishingLinks", "phoneNumbers", "suspiciousKeywords"]:
            if key in new_intel and new_intel[key]:
                session["intelligence"][key].update(new_intel[key])
    
    def increment_messages(self, session_id: str):
        session = self.get_session(session_id)
        session["message_count"] += 1
    
    def get_intel_as_lists(self, session_id: str) -> dict:
        """Convert sets back to lists for API response"""
        session = self.get_session(session_id)
        return {
            key: list(value) for key, value in session["intelligence"].items()
        }

session_store = SessionStore()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200, # Return 200 so GUVI sees the error message
        content={
            "status": "error", 
            "message": "Internal Server Error (Caught)", 
            "detail": str(exc),
            "type": type(exc).__name__
        }
    )

async def _process_agent_event(payload: ScammerInput, background_tasks: BackgroundTasks) -> dict:
    """Core logic to invoke the agent with session-based intelligence tracking"""
    session_id = payload.sessionId
    
    # 1. Update session message count
    session_store.increment_messages(session_id)
    
    # 2. Context Extraction (Channel Agnostic)
    channel = payload.metadata.get("channel", "whatsapp") if payload.metadata else "whatsapp"
    
    # 3. Agent Execution (Simple Async - No LangGraph)
    messages = payload.conversationHistory + [payload.message.model_dump()]
    final_state = await process_message(messages, channel=channel)
    
    # 4. Intelligence Aggregation
    if final_state.get("scamDetected"):
        # Mark session as scam detected
        session = session_store.get_session(session_id)
        session["scam_detected"] = True
        
        # Merge new intelligence with accumulated session intelligence
        raw_intel = final_state.get("extractedIntelligence", {})
        session_store.update_intelligence(session_id, raw_intel)
        
        # Get accumulated intelligence
        accumulated_intel = session_store.get_intel_as_lists(session_id)
        
        # Calculate total intelligence items
        total_intel_items = sum(len(v) for v in accumulated_intel.values())
        message_count = session["message_count"]
        
        # Trigger callback when we have sufficient intelligence OR conversation is long enough
        should_send_callback = (
            total_intel_items >= 3 or  # At least 3 pieces of intelligence
            message_count >= 5  # OR at least 5 messages exchanged
        )
        
        if should_send_callback:
            from src.schemas import CallbackPayload, ExtractedIntelligence
            from src.utils import send_guvi_callback
            
            intel_obj = ExtractedIntelligence(
                bankAccounts=accumulated_intel.get("bankAccounts", []),
                upiIds=accumulated_intel.get("upiIds", []),
                phishingLinks=accumulated_intel.get("phishingLinks", []),
                phoneNumbers=accumulated_intel.get("phoneNumbers", []),
                suspiciousKeywords=accumulated_intel.get("suspiciousKeywords", [])
            )
            
            # Generate agent notes
            keywords = ', '.join(accumulated_intel.get('suspiciousKeywords', [])[:3])
            notes = f"Accumulated intelligence across {message_count} turns. Scammer tactics: {keywords}"
            
            callback_data = CallbackPayload(
                sessionId=session_id,
                scamDetected=True,
                totalMessagesExchanged=message_count,
                extractedIntelligence=intel_obj,
                agentNotes=notes
            )
            
            background_tasks.add_task(send_guvi_callback, callback_data.model_dump())
            print(f"[CALLBACK] Triggered for session {session_id} with {total_intel_items} intel items")
        
    return final_state

# Middleware removed - was consuming request body and breaking JSON parsing
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch all exceptions and return 200 with error details for GUVI debugging"""
    print(f"[ERROR] Unhandled Exception: {type(exc).__name__}: {exc}")
    return JSONResponse(
        status_code=200,  # Return 200 so GUVI sees the error
        content={
            "status": "success",
            "reply": "I am having trouble understanding. Can you repeat that?",
            "debug_error": str(exc)
        }
    )

@app.post("/message")
async def chat_webhook(
    request: Request,

    background_tasks: BackgroundTasks,
    x_api_key: str = Header(...)
):
    """
    Standard API Endpoint matching GUVI requirements.
    Accepts raw JSON and manually validates for better error handling.
    """
    # 1. Security Check
    secret_key = os.getenv("API_SECRET_KEY")
    if not secret_key:
         print("WARNING: API_SECRET_KEY not set in .env. Using default for dev.")
         secret_key = "hackathon-secret-123"
         
    if x_api_key != secret_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")

    # 2. Get raw JSON payload
    try:
        payload_dict = await request.json()
        print(f"[DEBUG] Parsed JSON: {payload_dict}")
    except Exception as e:
        print(f"[ERROR] JSON Parse Failed: {e}")
        return {"status": "success", "reply": "I could not understand that message."}
    
    # 3. Manually construct ScammerInput
    try:
        payload = ScammerInput(**payload_dict)
    except Exception as e:
        print(f"[ERROR] Schema Validation Failed: {e}")
        print(f"[DEBUG] Raw Payload: {payload_dict}")
        return {"status": "success", "reply": "I am confused beta, please explain again."}

    # 4. Process the message
    final_state = await _process_agent_event(payload, background_tasks)

    # 5. Return Response (EXACTLY as GUVI expects)
    return {
        "status": "success",
        "reply": final_state.get("reply", "...")
    }

@app.post("/twilio/whatsapp")
async def twilio_webhook(
    From: str = Form(...),
    Body: str = Form(...),
    ProfileName: str | None = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks() 
):
    """
    Twilio Adapter: Receives Twilio Webhook -> Converts to ScammerInput -> Calls Agent
    """
    # 1. Convert Twilio format to Aaji format
    scammer_input = ScammerInput(
        sessionId=f"wa-{From}", # Unique session per phone number
        message=Message(
            sender="scammer",
            text=Body,
            timestamp="2024-02-01T12:00:00Z" # In real app use datetime.now()
        ),
        conversationHistory=[], 
        metadata={
            "channel": "whatsapp",
            "sender_name": ProfileName
        }
    )
    
    # 2. Invoke Brain
    final_state = await _process_agent_event(scammer_input, background_tasks)
    agent_reply = final_state.get("reply", "...")

    # 3. Respond to Twilio (XML)
    return Response(
        content=f"<Response><Message>{agent_reply}</Message></Response>", 
        media_type="application/xml"
    )

@app.get("/meta/instagram")
async def verify_instagram_webhook(
    mode: str = Query(..., alias="hub.mode"),
    token: str = Query(..., alias="hub.verify_token"),
    challenge: str = Query(..., alias="hub.challenge"),
):
    """
    Meta Verification Challenge
    """
    VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "aaji_meta_secret_123")
    
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return Response(content=challenge, media_type="text/plain")
    
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/meta/instagram")
async def instagram_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Handle Incoming Messages from Instagram
    """
    body = await request.json()
    
    # Check if this is a page/instagram entry
    if "entry" in body:
        for entry in body["entry"]:
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event.get("sender", {}).get("id")
                message_text = messaging_event.get("message", {}).get("text")
                
                if sender_id and message_text:
                    # Convert to ScammerInput
                    scammer_input = ScammerInput(
                        sessionId=f"ig-{sender_id}",
                        message=Message(
                            sender="scammer",
                            text=message_text,
                            timestamp="2024-02-01T12:00:00Z"
                        ),
                        conversationHistory=[],
                        metadata={"channel": "instagram", "sender_id": sender_id}
                    )
                    
                    # Using Background task for processing to reply asynchronously
                    # Note: Meta requires 200 OK fast. The reply logic would typically needs
                    # to call the Graph API to send a message back.
                    # Since we don't not have the Graph API Send logic implemented in `_process_agent_event`
                    # (it returns dict), we will simulate it safely.
                    
                    # For Hackathon: We just log the processing. 
                    # Real implementation requires calling:
                    # POST https://graph.facebook.com/v11.0/me/messages?access_token=...
                    
                    # In this synchronous flow for demo, we will process it but we can't "return" a reply
                    # to the webhook directly like Twilio.
                    
                    await _process_agent_event(scammer_input, background_tasks)
                    # For a real implementation, you would trigger an async function here to 
                    # await _process_agent_event -> get reply -> call Meta Send API.

    return Response(content="EVENT_RECEIVED", status_code=200)


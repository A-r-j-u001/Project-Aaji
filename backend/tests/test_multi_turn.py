"""
Multi-Turn Conversation Test for Agentic Honey-Pot
Simulates a scammer conversation and tests:
1. Session-based intelligence aggregation
2. Callback trigger logic
3. Response format compliance
"""
import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent
sys.path.append(str(backend_dir))

# Simulate the API workflow
from src.schemas import ScammerInput, Message
from src.main import session_store, _process_agent_event
from fastapi import BackgroundTasks
import asyncio

async def test_multi_turn_conversation():
    """Simulate a 4-turn scam conversation"""
    
    background_tasks = BackgroundTasks()
    session_id = "test-session-12345"
    
    # Turn 1: Initial scam message
    print("\n=== TURN 1 ===")
    payload1 = ScammerInput(
        sessionId=session_id,
        message=Message(
            sender="scammer",
            text="URGENT: Your bank account will be blocked in 2 hours. Verify immediately.",
            timestamp=1770005528731
        ),
        conversationHistory=[],
        metadata={"channel": "SMS", "language": "English", "locale": "IN"}
    )
    
    result1 = await _process_agent_event(payload1, background_tasks)
    print(f"Scam Detected: {result1.get('scamDetected')}")
    print(f"Reply: {result1.get('reply')}")
    
    # Check session state
    session = session_store.get_session(session_id)
    intel = session_store.get_intel_as_lists(session_id)
    print(f"Intelligence so far: {intel}")
    print(f"Message count: {session['message_count']}")
    
    # Turn 2: Scammer asks for UPI
    print("\n=== TURN 2 ===")
    payload2 = ScammerInput(
        sessionId=session_id,
        message=Message(
            sender="scammer",
            text="Share your UPI ID scammer123@paytm to receive verification code.",
            timestamp=1770005538731
        ),
        conversationHistory=[
            payload1.message.model_dump(),
            {"sender": "user", "text": result1.get('reply'), "timestamp": 1770005533731}
        ],
        metadata={"channel": "SMS", "language": "English", "locale": "IN"}
    )
    
    result2 = await _process_agent_event(payload2, background_tasks)
    print(f"Reply: {result2.get('reply')}")
    
    intel = session_store.get_intel_as_lists(session_id)
    print(f"Intelligence so far: {intel}")
    print(f"Message count: {session['message_count']}")
    
    # Turn 3: Scammer shares phone number
    print("\n=== TURN 3 ===")
    payload3 = ScammerInput(
        sessionId=session_id,
        message=Message(
            sender="scammer",
            text="Call our customer care at +919876543210 for assistance.",
            timestamp=1770005548731
        ),
        conversationHistory=[
            payload1.message.model_dump(),
            {"sender": "user", "text": result1.get('reply'), "timestamp": 1770005533731},
            payload2.message.model_dump(),
            {"sender": "user", "text": result2.get('reply'), "timestamp": 1770005543731}
        ],
        metadata={"channel": "SMS", "language": "English", "locale": "IN"}
    )
    
    result3 = await _process_agent_event(payload3, background_tasks)
    print(f"Reply: {result3.get('reply')}")
    
    intel = session_store.get_intel_as_lists(session_id)
    print(f"Intelligence so far: {intel}")
    print(f"Total intel items: {sum(len(v) for v in intel.values())}")
    print(f"Message count: {session['message_count']}")
    
    # Turn 4: Scammer shares link
    print("\n=== TURN 4 ===")
    payload4 = ScammerInput(
        sessionId=session_id,
        message=Message(
            sender="scammer",
            text="Click here to verify: http://fake-bank-verify.com/login",
            timestamp=1770005558731
        ),
        conversationHistory=[
            payload1.message.model_dump(),
            {"sender": "user", "text": result1.get('reply'), "timestamp": 1770005533731},
            payload2.message.model_dump(),
            {"sender": "user", "text": result2.get('reply'), "timestamp": 1770005543731},
            payload3.message.model_dump(),
            {"sender": "user", "text": result3.get('reply'), "timestamp": 1770005553731}
        ],
        metadata={"channel": "SMS", "language": "English", "locale": "IN"}
    )
    
    result4 = await _process_agent_event(payload4, background_tasks)
    print(f"Reply: {result4.get('reply')}")
    
    intel = session_store.get_intel_as_lists(session_id)
    print("\n=== FINAL INTELLIGENCE ===")
    print(f"Intelligence: {intel}")
    print(f"Total intel items: {sum(len(v) for v in intel.values())}")
    print(f"Total messages: {session['message_count']}")
    
    # Test callback should have been triggered by now
    print("\n=== TEST RESULT ===")
    total_items = sum(len(v) for v in intel.values())
    if total_items >= 3 or session['message_count'] >= 5:
        print("✅ PASS: Callback should have been triggered")
    else:
        print("❌ FAIL: Not enough intelligence or messages")
    
    print("\n=== SCHEMA VALIDATION ===")
    # Verify schema can handle the data
    from src.schemas import ExtractedIntelligence
    try:
        intel_obj = ExtractedIntelligence(**intel)
        print("✅ PASS: ExtractedIntelligence schema valid")
        print(f"Schema: {intel_obj.model_dump()}")
    except Exception as e:
        print(f"❌ FAIL: Schema error: {e}")

if __name__ == "__main__":
    asyncio.run(test_multi_turn_conversation())

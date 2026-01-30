import asyncio
import traceback

from src.main import aaji_graph


async def debug_run():
    print("Debugging Logic...")
    try:
        # Simulate Payload
        payload = {
            "sessionId": "test-debug",
            "message": {"text": "Send me money via UPI badguy@okaxis", "sender": "scammer"},
            "conversationHistory": []
        }
        
        # Manually construct state as in main.py
        initial_state = {
            "messages": payload["conversationHistory"] + [payload["message"]],
            "scam_detected": False,
            "intelligence": {},
            "final_response": {}
        }
        
        print("Invoking Graph...")
        result = await aaji_graph.ainvoke(initial_state)
        print("Success!")
        print(result)
        
    except Exception:
        with open("debug_error.log", "w") as f:
            f.write(traceback.format_exc())
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_run())

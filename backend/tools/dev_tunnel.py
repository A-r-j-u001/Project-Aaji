import os
import re
import sys
import time
import subprocess
import threading
from twilio.rest import Client

# Config
SSH_COMMAND = "ssh -R 80:localhost:8000 serveo.net"
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID") or sys.argv[1]
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN") or sys.argv[2]

def update_twilio_sandbox(url):
    """Updates the Twilio Sandbox Webhook"""
    print(f"\n[Auto-Updater] Found Tunnel URL: {url}")
    print("[Auto-Updater] Connecting to Twilio...")
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # NOTE: Twilio API doesn't have a direct "update sandbox" endpoint in the main library yet for some versions.
        # But we can try to update the 'IncomingPhoneNumber' if it was a real number.
        # For Sandbox, we might need to print instructions or use a specific known SID if available.
        # HOWEVER, let's try to query the account's regex-matched sandbox number or default.
        
        # Fallback: Since Sandbox API is tricky, we will PRINT the huge alert if we can't find it.
        # But actually, let's look for "Sandbox" friendly name or similar.
        
        incoming_numbers = client.incoming_phone_numbers.list(limit=20)
        target_number_sid = None
        
        for number in incoming_numbers:
            # Common patterns for sandbox or just update the FIRST one if user only has one (hackathon mode)
            print(f"[Auto-Updater] Checking number: {number.friendly_name} ({number.phone_number})")
            target_number_sid = number.sid
            break # Just take the first one for now as per 'Do this for me' request context
            
        if target_number_sid:
            client.incoming_phone_numbers(target_number_sid).update(
                sms_url=url,
                voice_url=url
            )
            print(f"✅ SUCCESS: Updated Twilio Number ({target_number_sid}) with new URL!")
        else:
            print("⚠️ COULD NOT FIND A PHONE NUMBER TO UPDATE via API.")
            print(f"Please manually paste: {url}")

    except Exception as e:
        print(f"❌ Twilio Update Failed: {e}")

def monitor_tunnel():
    """Runs SSH and parses output for URL"""
    print("[Auto-Updater] Starting SSH Tunnel...")
    process = subprocess.Popen(
        SSH_COMMAND, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    url_found = False
    
    while True:
        line = process.stdout.readline()
        if not line:
            break
        
        sys.stdout.write(line) # Mirror output
        
        # Regex to find https://....serveo.net or serveousercontent.com
        # Pattern: https://[a-z0-9-]+\.serveousercontent\.com
        if not url_found:
            match = re.search(r'(https://[a-z0-9-]+\.serveousercontent\.com)', line)
            if match:
                url = match.group(1) + "/twilio/whatsapp"
                # Update Twilio in a separate thread to not block
                threading.Thread(target=update_twilio_sandbox, args=(url,)).start()
                url_found = True

    process.wait()

if __name__ == "__main__":
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("Usage: python dev_tunnel.py <SID> <TOKEN>")
        sys.exit(1)
        
    monitor_tunnel()

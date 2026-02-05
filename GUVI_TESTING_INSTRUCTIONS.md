# GUVI Testing Instructions - Quick Reference

## 🔗 Public API Endpoint (Active Now)

**Base URL:** `https://rotten-fans-spend.loca.lt`

**Full Endpoint:** `https://rotten-fans-spend.loca.lt/message`

## 🔑 Authentication

**Header Name:** `x-api-key`  
**Header Value:** `hackathon-secret-123`

## 📝 GUVI Tester Instructions

### Step 1: Enter Headers
In the GUVI tester, enter:
```
x-api-key: hackathon-secret-123
```

### Step 2: Enter Honeypot API Endpoint URL
```
https://rotten-fans-spend.loca.lt/message
```

### Step 3: Click "Test Honeypot Endpoint"

## 🧪 Expected Test Behavior

The GUVI tester will send a scam message like:
```json
{
  "sessionId": "test-xxx",
  "message": {
    "sender": "scammer",
    "text": "Your bank account will be blocked. Verify immediately.",
    "timestamp": 1770005528731
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

Your API will respond with:
```json
{
  "status": "success",
  "reply": "Beta what is this? I am very old, please explain..."
}
```

And in the background, it will send intelligence to:
```
POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

## ✅ What GUVI Tests

1. **API Authentication** - x-api-key header validation
2. **Endpoint Availability** - Can reach your endpoint
3. **Request Handling** - Accepts correct JSON format
4. **Response Structure** - Returns `{status, reply}` format
5. **Response Behavior** - Proper honeypot engagement
6. **Basic Honeypot Logic** - Detects scam intent

## 🎯 Success Criteria

- ✅ Status code: 200
- ✅ Response has `status` field = "success"
- ✅ Response has `reply` field with string value
- ✅ Reply appears to be from honeypot persona

## 📊 Monitor Server Logs

Watch your terminal running uvicorn to see:
- Incoming requests from GUVI
- Scam detection results
- Callback triggers
- Intelligence extraction

---

**Tunnel Status:** 🟢 Active  
**Server Status:** 🟢 Running on localhost:8002  
**Ready for GUVI Testing:** ✅ YES

**Note:** This tunnel will remain active as long as the SSH connection is maintained. If it disconnects, run the tunnel command again.

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    model_config = ConfigDict(strict=True)
    sender: str
    text: str
    timestamp: str

class ScammerInput(BaseModel):
    model_config = ConfigDict(strict=True)
    sessionId: str
    message: Message
    conversationHistory: List[dict] = Field(default=[], alias="conversation_history") # Allow input as conversationHistory or conversation_history
    metadata: Optional[Dict[str, Any]] = None

class AgentResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    status: str
    reply: str

class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    suspiciousKeywords: List[str] = []

class CallbackPayload(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    """Message can have timestamp as int (epoch ms) or string (ISO format)"""
    sender: str
    text: str
    timestamp: Optional[Union[int, str, float]] = None  # GUVI sends epoch int, others may send string

    class Config:
        extra = "allow"

class ScammerInput(BaseModel):
    """Matches GUVI's exact payload format"""
    sessionId: str  # GUVI sends "sessionId" 
    message: Message
    conversationHistory: List[dict] = []  # GUVI sends "conversationHistory"
    metadata: Optional[Dict[str, Any]] = {}

    class Config:
        extra = "allow"  # Allow extra fields from GUVI

class AgentResponse(BaseModel):
    model_config = ConfigDict(strict=True)
    status: str
    reply: str

class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = Field(default_factory=list)
    upiIds: List[str] = Field(default_factory=list)
    phishingLinks: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    suspiciousKeywords: List[str] = Field(default_factory=list)

class CallbackPayload(BaseModel):
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Message(BaseModel):
    # model_config = ConfigDict(strict=False)
    sender: str
    text: str
    timestamp: Union[int, str, float, None] = None

    class Config:
        extra = "allow"

class ScammerInput(BaseModel):
    # model_config = ConfigDict(strict=False)
    sessionId: str = Field(..., alias="session_id") # Allow session_id
    message: Message
    conversationHistory: List[dict] = Field(default=[], alias="conversation_history") 
    metadata: Optional[Dict[str, Any]] = Field(default={})

    class Config:
        populate_by_name = True
        extra = "allow"

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

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Trade(BaseModel):
    trader_id: int
    trade_id: int
    symbol: str
    side: str
    quantity: int
    price: float
    timestamp: str


class SessionMemory(BaseModel):
    summary: str
    metrics: Dict[str, Any]
    tags: List[str] = Field(default_factory=list)


class TradeEvent(BaseModel):
    tradeId: str
    userId: str
    sessionId: str
    asset: str
    assetClass: str
    direction: str
    entryPrice: float
    exitPrice: float
    quantity: float
    entryAt: str
    exitAt: str
    status: str
    outcome: str
    pnl: float
    planAdherence: int
    emotionalState: str
    entryRationale: Optional[str] = None
    revengeFlag: bool = False


class CoachingRequest(BaseModel):
    trades: List[TradeEvent]


class SignalEvidence(BaseModel):
    signal: Literal["overtrading", "session_tilt", "revenge_trading"]
    sessionId: str
    tradeIds: List[str]
    reason: str


class CoachingResponse(BaseModel):
    userId: str
    message: str
    signals: List[SignalEvidence]


class AuditRequest(BaseModel):
    userId: str
    sessionIds: List[str] = Field(default_factory=list)
    responseText: Optional[str] = None


class AuditResult(BaseModel):
    sessionId: str
    status: Literal["found", "not found"]


class AuditResponse(BaseModel):
    userId: str
    results: List[AuditResult]


class TokenRequest(BaseModel):
    userId: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

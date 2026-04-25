from pydantic import BaseModel
from typing import Dict, Any, List, Optional

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
    tags: List[str]

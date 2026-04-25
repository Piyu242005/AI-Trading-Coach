from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.database import dataset
from app.services.profiler import analyze_trader_behavior

router = APIRouter()

@router.get("/{user_id}")
def get_user_profile(user_id: str):
    # Ensure dataset is read correctly; dataset["trades"] if that's the structure
    trades = dataset.get("trades", []) if isinstance(dataset, dict) else dataset
    
    profile = analyze_trader_behavior(user_id, trades)
    
    if profile["behavior"] == "none" and not profile["evidence"]:
        # We might have not found the user or they have no patterns
        return profile
        
    return profile

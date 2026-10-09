from copy import deepcopy
from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.auth import get_token_claims
from app.database import dataset

router = APIRouter()


@router.get("/trades")
def get_trades(claims: Dict[str, Any] = Depends(get_token_claims)):
    """Return only the authenticated user's records, never the entire seed dataset."""
    user_id = str(claims["sub"])
    result = deepcopy(dataset)
    result["traders"] = [
        trader for trader in result.get("traders", [])
        if str(trader.get("userId")) == user_id
    ]
    if "groundTruthLabels" in result:
        result["groundTruthLabels"] = [
            label for label in result["groundTruthLabels"]
            if str(label.get("userId")) == user_id
        ]
    return result

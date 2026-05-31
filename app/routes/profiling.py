from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.auth import require_user_match
from app.database import dataset
from app.services.dataset_utils import flatten_user_trades
from app.services.profiler import analyze_trader_behavior

router = APIRouter()


@router.get("/{user_id}")
def get_user_profile(
    user_id: str,
    _: Dict[str, Any] = Depends(require_user_match),
):
    trades = flatten_user_trades(dataset, user_id)

    profile = analyze_trader_behavior(user_id, trades)

    if profile["behavior"] == "none" and not profile["evidence"]:
        return profile

    return profile

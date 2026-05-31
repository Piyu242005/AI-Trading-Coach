from typing import Any, Dict
from fastapi import APIRouter, Depends
from app.auth import require_user_match
from app.database import dataset
from app.services.dataset_utils import flatten_user_trades
from app.services.profiler import analyze_trader_behavior

router = APIRouter()

@router.get("/{user_id}")
def get_discipline_score(
    user_id: str,
    _: Dict[str, Any] = Depends(require_user_match),
):
    trades = flatten_user_trades(dataset, user_id)
    profile = analyze_trader_behavior(user_id, trades)

    # Basic score logic
    total_trades = len(trades)
    wins = len([t for t in trades if t.get("outcome") == "win"])
    win_rate = (wins / total_trades * 100) if total_trades else 0
    
    win_rate_bonus = int(min(win_rate / 5, 15)) # up to 15 points
    
    # Calculate Profit Factor
    gross_profit = sum(t.get("pnl", 0) for t in trades if t.get("pnl", 0) > 0)
    gross_loss = abs(sum(t.get("pnl", 0) for t in trades if t.get("pnl", 0) < 0))
    profit_factor = (gross_profit / gross_loss) if gross_loss != 0 else 1.0
    pf_bonus = int(min(profit_factor * 5, 15)) # up to 15 points
    
    # Penalties
    overtrading_penalty = 0
    revenge_penalty = 0
    
    behavior = profile.get("behavior", "")
    if behavior == "overtrading":
        overtrading_penalty = -10
    elif behavior == "revenge_trading":
        revenge_penalty = -15
    elif behavior == "tilt":
        revenge_penalty = -12

    base_score = 70
    score = base_score + win_rate_bonus + pf_bonus + overtrading_penalty + revenge_penalty
    score = max(0, min(100, score))
    
    if score >= 85:
        risk_level = "Low"
    elif score >= 65:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    confidence = 85 + min(total_trades, 10) # 85-95% based on sample size

    return {
        "score": score,
        "risk_level": risk_level,
        "confidence": confidence,
        "contributors": {
            "win_rate_bonus": win_rate_bonus,
            "profit_factor_bonus": pf_bonus,
            "overtrading_penalty": overtrading_penalty,
            "revenge_trading_penalty": revenge_penalty
        }
    }

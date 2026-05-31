import json
from typing import Any, Dict

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.auth import require_user_match
from app.models import CoachingRequest, CoachingResponse
from app.services.coaching import (
    build_coaching_message,
    detect_signals_for_user_trades,
    tokenize_message,
)

router = APIRouter()


def _to_dict(model: Any) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


@router.post("/{user_id}", response_model=CoachingResponse)
def coach_user(
    user_id: str,
    payload: CoachingRequest,
    _: Dict[str, Any] = Depends(require_user_match),
):
    trades = [_to_dict(trade) for trade in payload.trades]
    signals = detect_signals_for_user_trades(user_id, trades)
    message = build_coaching_message(user_id, signals)

    return CoachingResponse(userId=user_id, message=message, signals=signals)


@router.post("/{user_id}/stream")
def coach_user_stream(
    user_id: str,
    payload: CoachingRequest,
    _: Dict[str, Any] = Depends(require_user_match),
):
    trades = [_to_dict(trade) for trade in payload.trades]
    signals = detect_signals_for_user_trades(user_id, trades)
    message = build_coaching_message(user_id, signals)

    async def event_generator():
        for token in tokenize_message(message):
            yield f"event: token\ndata: {token}\n\n"

        summary = {
            "userId": user_id,
            "signals": signals,
        }
        yield f"event: summary\ndata: {json.dumps(summary)}\n\n"
        yield "event: done\ndata: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

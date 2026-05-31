from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from app.auth import require_user_match
from app.models import SessionMemory
from app.mongodb import sessions_collection

router = APIRouter()


@router.put("/{user_id}/sessions/{session_id}")
def store_memory(
    user_id: str,
    session_id: str,
    memory: SessionMemory,
    _: Dict[str, Any] = Depends(require_user_match),
):
    record = memory.dict()
    record["user_id"] = user_id
    record["session_id"] = session_id

    sessions_collection.update_one(
        {"user_id": user_id, "session_id": session_id}, {"$set": record}, upsert=True
    )
    return {
        "status": "success",
        "message": "Memory stored successfully",
        "session_id": session_id,
    }


@router.get("/{user_id}/sessions/{session_id}")
def get_exact_memory(
    user_id: str,
    session_id: str,
    _: Dict[str, Any] = Depends(require_user_match),
):
    record = sessions_collection.find_one(
        {"user_id": user_id, "session_id": session_id}, {"_id": 0}
    )
    if not record:
        raise HTTPException(status_code=404, detail="Session not found")
    return record


@router.get("/{user_id}/context")
def get_memory_context(
    user_id: str,
    _: Dict[str, Any] = Depends(require_user_match),
):
    records = list(sessions_collection.find({"user_id": user_id}, {"_id": 0}))

    # Calculate patterns based on repetitive tags from real sessions
    all_tags = []
    for r in records:
        all_tags.extend(r.get("tags", []))

    tag_counts = {}
    for t in all_tags:
        tag_counts[t] = tag_counts.get(t, 0) + 1

    # If a tag represents a behavior and appears across multiple sessions, consider it a pattern
    patterns = [tag for tag, count in tag_counts.items() if count > 1]

    return {"sessions": records, "patternIds": patterns}

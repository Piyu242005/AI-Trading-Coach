import re
from typing import Any, Dict, List, Set

from fastapi import APIRouter, Depends

from app.auth import enforce_subject_match, get_token_claims
from app.database import dataset
from app.models import AuditRequest, AuditResponse, AuditResult
from app.mongodb import sessions_collection
from app.services.dataset_utils import get_user_session_ids

router = APIRouter()

SESSION_ID_PATTERN = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
)


def _extract_session_ids_from_text(text: str) -> List[str]:
    return sorted(set(SESSION_ID_PATTERN.findall(text)))


def _memory_session_ids(user_id: str) -> Set[str]:
    session_ids: Set[str] = set()
    rows = sessions_collection.find({"user_id": user_id}, {"_id": 0, "session_id": 1})
    for row in rows:
        session_id = row.get("session_id")
        if session_id is not None:
            session_ids.add(str(session_id))
    return session_ids


@router.post("/audit", response_model=AuditResponse)
def audit_session_references(
    payload: AuditRequest,
    claims: Dict[str, Any] = Depends(get_token_claims),
):
    enforce_subject_match(payload.userId, claims)

    requested_session_ids = list(payload.sessionIds)
    if payload.responseText:
        requested_session_ids.extend(_extract_session_ids_from_text(payload.responseText))

    # Keep deterministic output order while removing duplicates.
    deduped_session_ids = list(dict.fromkeys(requested_session_ids))

    valid_session_ids = get_user_session_ids(dataset, payload.userId)
    valid_session_ids.update(_memory_session_ids(payload.userId))

    results = [
        AuditResult(
            sessionId=session_id,
            status="found" if session_id in valid_session_ids else "not found",
        )
        for session_id in deduped_session_ids
    ]

    return AuditResponse(userId=payload.userId, results=results)

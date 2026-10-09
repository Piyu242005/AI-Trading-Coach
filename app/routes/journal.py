"""Authenticated, per-user persistent trading journal endpoints."""
from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth import get_token_claims
from app.models import JournalEntryCreate
from app.mongodb import journal_collection

router = APIRouter(prefix="/journal", tags=["journal"])


@router.get("")
def list_journal_entries(claims: Dict[str, Any] = Depends(get_token_claims)):
    user_id = str(claims["sub"])
    entries = list(
        journal_collection.find({"user_id": user_id}, {"_id": 0})
        .sort([("created_at", -1)])
    )
    return {"entries": entries}


@router.post("", status_code=status.HTTP_201_CREATED)
def create_journal_entry(
    payload: JournalEntryCreate,
    claims: Dict[str, Any] = Depends(get_token_claims),
):
    user_id = str(claims["sub"])
    record = payload.dict()
    record["date"] = payload.date.isoformat()
    record.update({
        "id": str(uuid4()),
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    journal_collection.insert_one(record)
    # PyMongo mutates the input mapping by adding an ObjectId; never expose it in JSON.
    return {key: value for key, value in record.items() if key != "_id"}


@router.delete("")
def clear_journal_entries(claims: Dict[str, Any] = Depends(get_token_claims)):
    user_id = str(claims["sub"])
    result = journal_collection.delete_many({"user_id": user_id})
    return {"deleted_count": result.deleted_count}


@router.delete("/{entry_id}")
def delete_journal_entry(
    entry_id: str,
    claims: Dict[str, Any] = Depends(get_token_claims),
):
    user_id = str(claims["sub"])
    result = journal_collection.delete_one({"id": entry_id, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Journal entry not found")
    return {"deleted": True, "id": entry_id}

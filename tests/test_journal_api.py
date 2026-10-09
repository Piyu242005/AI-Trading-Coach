import hashlib
import json
import os

import mongomock
from fastapi.testclient import TestClient

os.environ.setdefault("JWT_SECRET", "unit-test-jwt-secret-key-with-at-least-32-bytes")

from app.main import app  # noqa: E402

client = TestClient(app)
TEST_PASSWORD = "journal-test-password"


def auth_headers(user_id: str):
    salt = b"journal-test-salt"
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", TEST_PASSWORD.encode("utf-8"), salt, 310_000
    ).hex()
    os.environ["AI_TRADING_COACH_USERS_JSON"] = json.dumps(
        {user_id: f"{salt.hex()}:{password_hash}"}
    )
    response = client.post(
        "/api/auth/token",
        json={"userId": user_id, "password": TEST_PASSWORD},
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def setup_function():
    import app.routes.journal as journal_route

    client_mock = mongomock.MongoClient()
    journal_route.journal_collection = client_mock["test_db"]["journal_entries"]


def sample_payload():
    return {
        "date": "2026-10-09",
        "asset": "NIFTY",
        "direction": "Long",
        "entry": 25000,
        "exit": 25100,
        "strategy": "Breakout retest",
        "pnl": 100,
        "confidence": 7,
        "notes": "Waited for confirmation.",
    }


def test_journal_requires_authentication():
    response = client.get("/api/journal")
    assert response.status_code == 401


def test_journal_create_list_and_clear_are_scoped_to_user():
    headers_a = auth_headers("journal-user-a")
    headers_b = auth_headers("journal-user-b")

    created = client.post("/api/journal", json=sample_payload(), headers=headers_a)
    assert created.status_code == 201
    entry = created.json()
    assert entry["asset"] == "NIFTY"
    assert entry["user_id"] == "journal-user-a"
    assert entry["id"]

    list_a = client.get("/api/journal", headers=headers_a)
    list_b = client.get("/api/journal", headers=headers_b)
    assert list_a.status_code == 200
    assert len(list_a.json()["entries"]) == 1
    assert list_b.status_code == 200
    assert list_b.json()["entries"] == []

    cleared = client.delete("/api/journal", headers=headers_b)
    assert cleared.status_code == 200
    assert cleared.json()["deleted_count"] == 0
    assert len(client.get("/api/journal", headers=headers_a).json()["entries"]) == 1

    cleared_owner = client.delete("/api/journal", headers=headers_a)
    assert cleared_owner.status_code == 200
    assert client.get("/api/journal", headers=headers_a).json()["entries"] == []


def test_journal_entry_validation_and_owner_only_delete():
    headers_a = auth_headers("journal-owner")
    headers_b = auth_headers("journal-other")

    invalid = client.post(
        "/api/journal", json={**sample_payload(), "confidence": 99}, headers=headers_a
    )
    assert invalid.status_code == 422

    created = client.post("/api/journal", json=sample_payload(), headers=headers_a)
    entry_id = created.json()["id"]
    denied = client.delete(f"/api/journal/{entry_id}", headers=headers_b)
    assert denied.status_code == 404
    deleted = client.delete(f"/api/journal/{entry_id}", headers=headers_a)
    assert deleted.status_code == 200

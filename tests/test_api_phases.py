import time

import mongomock
from fastapi.testclient import TestClient

from app.database import dataset
from app.main import app


client = TestClient(app)


def _auth_headers(user_id: str):
    token_response = client.post("/api/auth/token", json={"userId": user_id})
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _sample_user(index: int = 0) -> str:
    return dataset["groundTruthLabels"][index]["userId"]


def _sample_session_id(user_index: int = 0, session_index: int = 0) -> str:
    return dataset["traders"][user_index]["sessions"][session_index]["sessionId"]


def _sample_trades(user_index: int = 0, session_index: int = 0):
    return dataset["traders"][user_index]["sessions"][session_index]["trades"]


def _patch_mongo_collections(mock_collection):
    import app.mongodb as mongodb
    import app.routes.audit as audit_route
    import app.routes.memory as memory_route

    mongodb.sessions_collection = mock_collection
    memory_route.sessions_collection = mock_collection
    audit_route.sessions_collection = mock_collection


def setup_function():
    mock_client = mongomock.MongoClient()
    collection = mock_client["nevup_memory"]["sessions"]
    _patch_mongo_collections(collection)


def test_memory_persistence_put_and_get_exact_data():
    user_id = _sample_user(0)
    session_id = "session-for-test-memory"
    headers = _auth_headers(user_id)

    put_payload = {
        "summary": "Trader stayed disciplined after drawdown.",
        "metrics": {"winRate": 0.4, "maxDrawdown": -120.5},
    }
    put_response = client.put(
        f"/api/memory/{user_id}/sessions/{session_id}",
        json=put_payload,
        headers=headers,
    )
    assert put_response.status_code == 200

    get_response = client.get(
        f"/api/memory/{user_id}/sessions/{session_id}",
        headers=headers,
    )
    assert get_response.status_code == 200
    body = get_response.json()
    assert body["summary"] == put_payload["summary"]
    assert body["metrics"] == put_payload["metrics"]
    assert body["user_id"] == user_id
    assert body["session_id"] == session_id


def test_auth_rejects_mismatched_user_id():
    owner_user_id = _sample_user(0)
    other_user_id = _sample_user(1)
    headers = _auth_headers(owner_user_id)

    response = client.put(
        f"/api/memory/{other_user_id}/sessions/forbidden-session",
        json={"summary": "blocked", "metrics": {}},
        headers=headers,
    )
    assert response.status_code == 403


def test_audit_returns_found_and_not_found_for_session_ids():
    user_id = _sample_user(0)
    real_session_id = _sample_session_id(0, 0)
    fake_session_id = "00000000-0000-0000-0000-000000000000"
    headers = _auth_headers(user_id)

    response = client.post(
        "/audit",
        json={"userId": user_id, "sessionIds": [real_session_id, fake_session_id]},
        headers=headers,
    )
    assert response.status_code == 200

    results = {item["sessionId"]: item["status"] for item in response.json()["results"]}
    assert results[real_session_id] == "found"
    assert results[fake_session_id] == "not found"


def test_streaming_coaching_is_sse_and_under_3_seconds():
    user_id = _sample_user(0)
    headers = _auth_headers(user_id)

    start_time = time.perf_counter()
    response = client.post(
        f"/api/coaching/{user_id}/stream",
        json={"trades": _sample_trades(0, 0)},
        headers=headers,
    )
    elapsed = time.perf_counter() - start_time

    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")
    assert "event: token" in response.text
    assert "event: done" in response.text
    assert elapsed < 3


def test_evaluation_report_json_and_html():
    json_response = client.get("/evaluation/report")
    assert json_response.status_code == 200
    json_body = json_response.json()
    assert "overall" in json_body
    assert "precision" in json_body["overall"]
    assert "recall" in json_body["overall"]
    assert "f1" in json_body["overall"]

    html_response = client.get("/evaluation/report?format=html")
    assert html_response.status_code == 200
    assert "text/html" in html_response.headers.get("content-type", "")
    assert "NevUp Evaluation Report" in html_response.text

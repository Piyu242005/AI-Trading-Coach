import hashlib
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

JWT_SECRET = os.getenv("JWT_SECRET", "")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRES_MINUTES = int(os.getenv("JWT_EXPIRES_MINUTES", "60"))

bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(sub: str, expires_minutes: Optional[int] = None) -> str:
    if len(JWT_SECRET) < 32:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="JWT_SECRET is not configured securely")
    now = datetime.now(timezone.utc)
    expiry_minutes = expires_minutes or JWT_EXPIRES_MINUTES
    payload = {
        "sub": sub,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expiry_minutes)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_token_claims(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> Dict[str, Any]:
    if len(JWT_SECRET) < 32:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="JWT_SECRET is not configured securely")

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        ) from exc
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    if not payload.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject",
        )

    return payload


def require_user_match(
    user_id: str,
    claims: Dict[str, Any] = Depends(get_token_claims),
) -> Dict[str, Any]:
    if str(claims.get("sub")) != str(user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token subject does not match userId",
        )
    return claims


def enforce_subject_match(expected_user_id: str, claims: Dict[str, Any]) -> None:
    if str(claims.get("sub")) != str(expected_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token subject does not match userId",
        )


def verify_configured_user(user_id: str, password: str) -> bool:
    """Verify credentials against an environment-configured PBKDF2 password map.

    AI_TRADING_COACH_USERS_JSON maps user IDs to "salt_hex:pbkdf2_hash_hex".
    There is deliberately no insecure default user or password.
    """
    raw_users = os.getenv("AI_TRADING_COACH_USERS_JSON", "")
    if not raw_users:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication is not configured on this server",
        )
    try:
        users = json.loads(raw_users)
    except (TypeError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication configuration is invalid",
        ) from exc
    if not isinstance(users, dict) or not users:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No authenticated users are configured",
        )

    encoded = users.get(user_id)
    if not isinstance(encoded, str) or ":" not in encoded:
        # Do a comparable-cost hash for unknown users to reduce timing differences.
        hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), b"unknown-user-salt", 310_000)
        return False

    salt_hex, expected_hex = encoded.split(":", 1)
    try:
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(expected_hex)
    except ValueError:
        return False
    if len(salt) < 16 or len(expected) != 32:
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000)
    return secrets.compare_digest(actual, expected)

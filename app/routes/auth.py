from fastapi import APIRouter, HTTPException, status

from app.auth import create_access_token, verify_configured_user
from app.models import TokenRequest, TokenResponse

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
def issue_token(payload: TokenRequest):
    if not verify_configured_user(payload.userId, payload.password.get_secret_value()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user ID or password")
    token = create_access_token(payload.userId)
    return TokenResponse(access_token=token)

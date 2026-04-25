from fastapi import APIRouter

from app.auth import create_access_token
from app.models import TokenRequest, TokenResponse

router = APIRouter()


@router.post("/token", response_model=TokenResponse)
def issue_token(payload: TokenRequest):
    token = create_access_token(payload.userId)
    return TokenResponse(access_token=token)

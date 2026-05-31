from fastapi import APIRouter
from app.database import dataset

router = APIRouter()


@router.get("/trades")
def get_trades():
    return dataset

from fastapi import APIRouter
from app.services.user_service import get_user_info

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
def read_user(user_id: int):
    return get_user_info(user_id)
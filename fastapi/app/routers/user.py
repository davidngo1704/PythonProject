from fastapi import APIRouter
from app.services.user_service import get_user_info

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}")
async def read_user(user_id: int):
    return await get_user_info(user_id)
from app.database import db
from app.models.user_model import User

async def get_user_info(user_id: int) -> User:
    user_data = await db["users"].find_one({"id": user_id})
    if user_data:
        return User(**user_data)
    return User(id=user_id, name="Không tìm thấy", email="na")
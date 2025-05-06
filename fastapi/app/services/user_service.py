from app.models.user_model import User

def get_user_info(user_id: int) -> User:
    # giả lập lấy dữ liệu từ DB
    return User(id=user_id, name="Chồng yêu", email="chongyeu@example.com")
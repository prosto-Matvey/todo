from database import get_db_cursor
from schemas.UserSchema import User

def register_user(user: User):
    with get_db_cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", 
            (user.username, user.password)
        )
        return {"message": "Пользователь зарегистрирован"}
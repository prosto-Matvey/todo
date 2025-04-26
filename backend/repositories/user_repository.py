from schemas.UserSchema import User
from database import get_db_cursor
from passlib.context import CryptContext

# Настройка хеширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_user(user: User):
    # Хешируем пароль
    hashed_password = pwd_context.hash(user.password)
    with get_db_cursor() as cursor:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", 
            (user.username, hashed_password)
        )
        return {"message": "Пользователь зарегистрирован"}

def get_user(username: str):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "username": row[1], "password": row[2]}
    return None
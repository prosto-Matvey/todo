import sqlite3
from contextlib import contextmanager

DATABASE_URL = "tasks.db"

def get_db_connection():
    """Создает подключени к базе данных и возвращает его"""
    return sqlite3.connect(DATABASE_URL)

@contextmanager
def get_db_cursor():
    """Контекстный менеджер для работы с операциями базы данных"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    """Инициализация базы данных с нужными таблицами"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                is_completed BOOLEAN NOT NULL DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
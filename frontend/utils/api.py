import streamlit as st
import requests
from requests.exceptions import RequestException
from schemas.task import Task

# Настройка URL API
API_URL = "http://localhost:8000"  # Измените, если ваш FastAPI работает на другом порту

def login_user(username, password):
    """Попытка входа пользователя через API"""
    try:
        response = requests.post(
            f"{API_URL}/login",
            params={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            # Сохранение cookies из ответа
            st.session_state.cookies = response.cookies
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.error_message = ""
            st.session_state.page = "dashboard"
            return True
        else:
            error_detail = response.json().get("detail", "Неизвестная ошибка")
            st.session_state.error_message = f"Ошибка входа: {error_detail}"
            return False
    except RequestException as e:
        st.session_state.error_message = f"Ошибка соединения: {str(e)}"
        return False

def register_user(username, password):
    """Регистрация нового пользователя через API"""
    try:
        response = requests.post(
            f"{API_URL}/register",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            st.session_state.error_message = ""
            return True, "Регистрация успешна! Теперь вы можете войти."
        else:
            error_detail = response.json().get("detail", "Неизвестная ошибка")
            st.session_state.error_message = f"Ошибка регистрации: {error_detail}"
            return False, st.session_state.error_message
    except RequestException as e:
        st.session_state.error_message = f"Ошибка соединения: {str(e)}"
        return False, st.session_state.error_message
    
def get_tasks() -> list[Task]:
    """Получение всех задач пользователя"""
    try:
        response = requests.get(
            f"{API_URL}/tasks",
            cookies=st.session_state.cookies
        )
        
        if response.status_code == 200:
            tasks_data = response.json()
            return [Task(**task) for task in tasks_data]
        else:
            error_detail = response.json().get("detail", "Неизвестная ошибка")
            st.session_state.error_message = f"Ошибка получения задач: {error_detail}"
            if response.status_code == 401:  # Unauthorized
                st.session_state.logged_in = False
                st.session_state.page = "login"
            return []
    except RequestException as e:
        st.session_state.error_message = f"Ошибка соединения: {str(e)}"
        return []
    
def create_task(title, description=""):
    """Создание новой задачи"""
    try:
        response = requests.post(
            f"{API_URL}/task",
            json={"title": title, "description": description, "is_completed": False},
            cookies=st.session_state.cookies
        )
        
        if response.status_code == 200:
            return True, "Задача успешно создана"
        else:
            error_detail = response.json().get("detail", "Неизвестная ошибка")
            return False, f"Ошибка создания задачи: {error_detail}"
    except RequestException as e:
        return False, f"Ошибка соединения: {str(e)}"
    
def update_task(task_id, title, description, is_completed):
    """Обновление существующей задачи"""
    try:
        response = requests.put(
            f"{API_URL}/task/{task_id}",
            json={"title": title, "description": description, "is_completed": is_completed},
            cookies=st.session_state.cookies
        )
        
        if response.status_code == 200:
            return True, "Задача успешно обновлена"
        else:
            error_detail = response.json().get("detail", "Неизвестная ошибка")
            return False, f"Ошибка обновления задачи: {error_detail}"
    except RequestException as e:
        return False, f"Ошибка соединения: {str(e)}"

def delete_task(task_id):
    """Удаление задачи"""
    try:
        response = requests.delete(
            f"{API_URL}/task/{task_id}",
            cookies=st.session_state.cookies
        )
        
        if response.status_code == 200:
            return True, "Задача успешно удалена"
        else:
            error_detail = response.json().get("detail", "Неизвестная ошибка")
            return False, f"Ошибка удаления задачи: {error_detail}"
    except RequestException as e:
        return False, f"Ошибка соединения: {str(e)}"
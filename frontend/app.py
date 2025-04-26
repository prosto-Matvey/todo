import streamlit as st
from pages.login import show_login_page
from pages.register import show_register_page
from pages.dashboard import show_dashboard
from utils.session import initialize_session

# Настройка конфигурации страницы с опцией hide_sidebar
st.set_page_config(
    page_title="Todo App",
    page_icon="✅",
    layout="centered"
)

# Инициализация переменных состояния сессии
initialize_session()

if st.session_state.page == "login":
    show_login_page()
elif st.session_state.page == "register":
    show_register_page()
elif st.session_state.page == "dashboard":
    show_dashboard()
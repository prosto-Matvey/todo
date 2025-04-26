import streamlit as st
from utils.api import get_tasks, create_task, update_task, delete_task
from schemas.task import Task
from pydantic import BaseModel


# Function to display the dashboard
def show_dashboard():
    st.title("Todo App")

    # Split the page into two columns: one for adding tasks, one for managing tasks
    col1, col2 = st.columns(2)

    # --- Column 1: Add New Task ---
    with col1:
        with st.form("new_task_form"):
            title = st.text_input("Название задачи", placeholder="Введите название задачи")
            description = st.text_area("Описание", placeholder="Введите описание задачи")
            submitted = st.form_submit_button("Добавить задачу")

            if submitted:
                if title.strip() == "":
                    st.error("Заголовок не может быть пустым.")
                else:
                    create_task(title, description)
                    st.success("Задача успешно добавлена!")
                    st.rerun()
    
    # --- Column 2: View, Edit, and Manage Tasks ---
    with col2:
        # Используем session_state для отслеживания состояния редактирования
        if 'editing_task_id' not in st.session_state:
            st.session_state.editing_task_id = None
            
        tasks = get_tasks()
        if not tasks:
            st.info("Пока нет задач.")
        else:
            # Используем отдельные контейнеры для каждой задачи
            for i, task in enumerate(tasks):
                task_container = st.container()
                
                with task_container:
                    with st.expander(f"Задача: {task.title}"):
                        # Если задача не в режиме редактирования, показываем информацию и кнопки
                        if st.session_state.editing_task_id != task.id:
                            st.write(f"**Описание:** {task.description}")
                            st.write(f"**Статус:** {'Выполнено' if task.is_completed else 'Не выполнено'}")

                            # Edit and Delete options
                            col_edit, col_delete = st.columns(2)
                            
                            with col_edit:
                                # Используем уникальный ключ для каждой кнопки
                                if st.button("Изменить", key=f"update_btn_{task.id}_{i}"):
                                    st.session_state.editing_task_id = task.id
                                    st.rerun()
                            
                            with col_delete:
                                # Используем уникальный ключ для каждой кнопки
                                if st.button("Удалить", key=f"delete_btn_{task.id}_{i}"):
                                    delete_task(task.id)
                                    st.success("Задача успешно удалена!")
                                    st.rerun()
                        
                        else:
                            with st.form(key=f"edit_task_form_{task.id}_{i}"):
                                edited_title = st.text_input("Название задачи", value=task.title)
                                edited_description = st.text_area("Описание", value=task.description)
                                edited_status = st.checkbox("Выполнено", value=task.is_completed)
                                
                                col_save, col_cancel = st.columns(2)
                                
                                with col_save:
                                    save_button = st.form_submit_button("Сохранить")
                                
                                with col_cancel:
                                    cancel_button = st.form_submit_button("Отмена")
                                
                                if save_button:
                                    if edited_title.strip() == "":
                                        st.error("Заголовок не может быть пустым.")
                                    else:
                                        # Вызываем функцию обновления задачи
                                        success, message = update_task(task.id, edited_title, edited_description, edited_status)
                                        if success:
                                            st.session_state.editing_task_id = None
                                            st.success("Задача успешно обновлена!")
                                            st.rerun()
                                        else:
                                            st.error(f"Ошибка при обновлении задачи: {message}")
                                
                                if cancel_button:
                                    st.session_state.editing_task_id = None
                                    st.rerun()
                                    

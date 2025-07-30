import streamlit as st
from mcr.process_input import process_input
from database.mydatabase import *
from utils import process_anskeys

def render_upload_answer_section(name_file: str):
    """
    Render a file upload section in the Streamlit UI.

    Args:
        name_file (str): The type or name of the file expected to be uploaded (e.g., "Answer" or "Assignment").

    Behavior:
        - Displays a sub-header prompting the user to upload or drop the specified file type.
        - Provides a file uploader that accepts one or more CSV files.
        - Displays a success message for each uploaded file showing its name.
        - Includes a "Delete" button for future functionality (currently non-functional).

    Note:
        This function relies on Streamlit components such as `st.markdown`, `st.file_uploader`, 
        and `st.button` for rendering the UI.
    """
    st.markdown("#### Upload or Drop {} file".format(name_file))
    uploaded_files = st.file_uploader(
        "Upload file Answer", type="xlsx", accept_multiple_files=True, label_visibility="collapsed"
    )
    if uploaded_files:
        for file in uploaded_files:
            course_id, test_form_code, questions = process_anskeys(file)
            insert_answer(course_id, test_form_code, questions)
    st.button("Delete", key="delete")

def render_upload_assignment_section(name_file: str):
    """
    Render a file upload section in the Streamlit UI.

    Args:
        name_file (str): The type or name of the file expected to be uploaded (e.g., "Answer" or "Assignment").

    Behavior:
        - Displays a sub-header prompting the user to upload or drop the specified file type.
        - Provides a file uploader that accepts one or more CSV files.
        - Displays a success message for each uploaded file showing its name.
        - Includes a "Delete" button for future functionality (currently non-functional).

    Note:
        This function relies on Streamlit components such as `st.markdown`, `st.file_uploader`, 
        and `st.button` for rendering the UI.
    """
    st.markdown("#### Upload or Drop {} file".format(name_file))
    uploaded_files = st.file_uploader(
        "Upload file Assignment", type=["png", "jpg", "jpeg"], accept_multiple_files=True, label_visibility="collapsed"
    )
    if uploaded_files:
        with st.spinner("Processing image..."):
            for file in uploaded_files:
                data = process_input(file.read(), file.name)
                if data is not None:
                    insert_assignment(data)        
    st.button("Delete", key="delete")
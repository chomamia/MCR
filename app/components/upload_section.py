import streamlit as st
from mcr.process_input import process_input
from mcr.yolo_detect import yolo_process_input
from database.answer import *
from database.assignment import *
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
    st.markdown(f"#### Upload or Drop {name_file} file")
    if "upload_key" not in st.session_state:
        st.session_state.upload_key = 0
    uploaded_files = st.file_uploader(
        "Upload file Answer", type="xlsx", accept_multiple_files=True, key=f"uploader_{st.session_state.upload_key}", label_visibility="collapsed"
    )
    if uploaded_files:
        for file in uploaded_files:
            course_id, test_form_code, questions = process_anskeys(file)
            user_id = st.session_state["id"]
            if course_id == "" or test_form_code == "":
                st.error(f"Upload Error: Course ID and Test Form Code is required")
            else:
                exist = check_answer_exist(user_id, course_id, test_form_code)
                if exist:
                    st.error(f"Course ID and Test Form Code is exist")
                else:
                    insert_answer(user_id, file.name, course_id, test_form_code, questions)
                    st.success(f"Uploaded: {file.name}")
                    
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
    method = st.radio(
        "Choose detection method:",
        ["Detect by YOLO", "Image Processing"],
        horizontal=True
    )
    if "upload_assignment_key" not in st.session_state:
        st.session_state.upload_assignment_key = 0
    uploaded_files = st.file_uploader(
        "Upload file Assignment", type=["png", "jpg", "jpeg"], accept_multiple_files=True, key=f"uploader_{st.session_state.upload_assignment_key}", label_visibility="collapsed"
    )
    if uploaded_files:
        user_id = st.session_state["id"]
        with st.spinner("Processing image..."):
            for file in uploaded_files:
                if method == "Detect by YOLO":
                    data = yolo_process_input(file.read(), file.name)
                else:
                    data = process_input(file.read(), file.name)
                last_name, first_name, middle_name, test_form_code, student_id, course_id, source_file, assignment_list = convert_insert_assignment(data)
                if test_form_code == "" or student_id =="" or course_id == "":
                    st.error(f"Personal information such as Test Form Code, Student ID, course ID, are required")
                else:
                    exist = check_assignment_exist(user_id, test_form_code, student_id, course_id)
                    if exist:
                        st.error(f"Test Form Code, Student ID, course ID is exist")                
                    elif data is not None:
                        check_upload = insert_assignment(user_id, data)
                        if check_upload:        
                            st.success(f"Uploaded: {file.name}")

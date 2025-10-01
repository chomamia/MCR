import streamlit as st
from components.upload_section import render_upload_answer_section
from components.table_section import render_table_section_answer
from database.answer import get_all_answers
from utils import get_localized_string

def show():
    """
    Display the "Answer Management" page using Streamlit.

    Behavior:
        - Displays the page title and a separator line.
        - Renders the upload section for answer files using `render_upload_section("Answer")`.
        - Generates a sample dataset of answer file metadata by calling `create_answer_data()`.
        - Displays the dataset in a table using `render_table_section_answer()`.

    Note:
        This function depends on Streamlit UI components and external helper functions 
        `render_upload_section` and `render_table_section_answer`.
    """
    lang = st.session_state.get("lang", "en")
    st.markdown(f"### 📄 {get_localized_string('answer_management', lang)}")
    st.markdown("---")
    render_upload_answer_section(get_localized_string("answer", lang))
    user_id = st.session_state["id"]
    df = get_all_answers(user_id)
    render_table_section_answer(df)
    
